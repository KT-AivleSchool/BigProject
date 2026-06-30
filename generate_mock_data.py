import os
import random
import pandas as pd
import json

# 저장 디렉토리 설정 (프로젝트 하위의 dataset 폴더)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)

# 시범 자치구: 서울시 관악구 중심 바운더리 설정 (위도: 37.46 ~ 37.49, 경도: 126.91 ~ 126.97)
LAT_MIN, LAT_MAX = 37.4600, 37.4900
LNG_MIN, LNG_MAX = 126.9100, 126.9700

# 관악구 행정동 목록 및 행정동 법정코드 (sig_cd: 11620)
DONG_LIST = [
    {"code": "1162056500", "name": "낙성대동"},
    {"code": "1162057500", "name": "난곡동"},
    {"code": "1162058500", "name": "난향동"},
    {"code": "1162059500", "name": "남현동"},
    {"code": "1162060500", "name": "대학동"},
    {"code": "1162061500", "name": "미성동"},
    {"code": "1162062500", "name": "보라매동"},
    {"code": "1162063500", "name": "봉천동"},
    {"code": "1162064500", "name": "삼성동"},
    {"code": "1162065500", "name": "서원동"},
    {"code": "1162066500", "name": "서림동"},
    {"code": "1162067500", "name": "신림동"},
    {"code": "1162068500", "name": "신사동"},
    {"code": "1162069500", "name": "신원동"},
    {"code": "1162070500", "name": "은천동"},
    {"code": "1162071500", "name": "인헌동"},
    {"code": "1162072500", "name": "조원동"},
    {"code": "1162073500", "name": "중앙동"},
    {"code": "1162074500", "name": "청룡동"},
    {"code": "1162075500", "name": "청림동"},
    {"code": "1162076500", "name": "행운동"}
]

def generate_random_coords(n):
    """지정 바운더리 내 n개의 랜덤 좌표 생성"""
    coords = []
    for _ in range(n):
        lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
        lng = round(random.uniform(LNG_MIN, LNG_MAX), 6)
        coords.append((lat, lng))
    return coords

def generate_nosmoking_zones():
    """1. 금연구역 모의 데이터 생성 (nosmoking_zones.csv)"""
    print("Generating Mock Nosmoking Zones...")
    coords = generate_random_coords(50)
    data = []
    for i, (lat, lng) in enumerate(coords):
        dong = random.choice(DONG_LIST)
        data.append({
            "zone_id": f"NS_{1000 + i}",
            "zone_name": f"{dong['name']} 금연구역 {i+1}호",
            "sig_cd": "11620",
            "dong_code": dong["code"],
            "address": f"서울특별시 관악구 {dong['name']} {random.randint(1, 500)}길",
            "latitude": lat,
            "longitude": lng,
            "area_size": round(random.uniform(10.0, 150.0), 2),
            "created_at": "2026-01-01 09:00:00"
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(DATASET_DIR, "nosmoking_zones.csv"), index=False, encoding="utf-8-sig")

def generate_kindergartens():
    """2. 어린이집 모의 데이터 생성 (kindergartens.csv)"""
    print("Generating Mock Kindergartens...")
    coords = generate_random_coords(30)
    data = []
    for i, (lat, lng) in enumerate(coords):
        dong = random.choice(DONG_LIST)
        data.append({
            "kindergarten_id": f"KG_{2000 + i}",
            "kindergarten_name": f"관악 {dong['name']} 어린이집 {i+1}호",
            "sig_cd": "11620",
            "dong_code": dong["code"],
            "latitude": lat,
            "longitude": lng,
            "capacity": random.randint(15, 120)
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(DATASET_DIR, "kindergartens.csv"), index=False, encoding="utf-8-sig")

def generate_transit_data():
    """3. 대중교통 노드 및 승하차 이용량 모의 데이터 생성 (transit_stations.csv, transit_volume.csv)"""
    print("Generating Mock Transit Data...")
    
    # 정류소 마스터 정보 생성
    bus_coords = generate_random_coords(60)
    station_data = []
    volume_data = []
    
    for i, (lat, lng) in enumerate(bus_coords):
        dong = random.choice(DONG_LIST)
        station_id = f"BS_{3000 + i}"
        station_no = f"21{random.randint(100, 999):03d}"
        
        # 역사/정류소 위치 마스터
        station_data.append({
            "station_id": station_id,
            "station_no": station_no,
            "station_name": f"{dong['name']} 버스정류장 {i+1}호",
            "type": "BUS",
            "latitude": lat,
            "longitude": lng
        })
        
        # 월평균 승하차 이용량 통계
        volume_data.append({
            "station_no": station_no,
            "station_name": f"{dong['name']} 버스정류장 {i+1}호",
            "boarding_passengers": random.randint(5000, 80000),
            "alighting_passengers": random.randint(5000, 75000)
        })
        
    # 지하철역 정보 생성 (5개역)
    subway_coords = generate_random_coords(5)
    for i, (lat, lng) in enumerate(subway_coords):
        dong = random.choice(DONG_LIST)
        station_id = f"SW_{4000 + i}"
        station_no = f"02{30 + i}" # 2호선 가정
        
        station_data.append({
            "station_id": station_id,
            "station_no": station_no,
            "station_name": f"{dong['name']}역 (2호선)",
            "type": "SUBWAY",
            "latitude": lat,
            "longitude": lng
        })
        
        volume_data.append({
            "station_no": station_no,
            "station_name": f"{dong['name']}역 (2호선)",
            "boarding_passengers": random.randint(100000, 800000),
            "alighting_passengers": random.randint(100000, 780000)
        })
        
    df_stations = pd.DataFrame(station_data)
    df_stations.to_csv(os.path.join(DATASET_DIR, "transit_stations.csv"), index=False, encoding="utf-8-sig")
    
    df_volume = pd.DataFrame(volume_data)
    df_volume.to_csv(os.path.join(DATASET_DIR, "transit_volume.csv"), index=False, encoding="utf-8-sig")

def generate_population_density():
    """4. 생활인구 경량화 모의 데이터 생성 (population_density.csv)"""
    print("Generating Mock Population Density...")
    data = []
    
    # 시간대 정의 (출퇴근, 낮, 밤)
    time_slots = ["COMMUTE", "DAYTIME", "NIGHTTIME"]
    # 요일 정의 (주중, 주말)
    day_types = ["WEEKDAY", "WEEKEND"]
    
    for dong in DONG_LIST:
        for day in day_types:
            for time in time_slots:
                # 가상 생활인구 산출
                base_pop = random.randint(15000, 50000)
                if time == "COMMUTE":
                    pop = int(base_pop * random.uniform(1.2, 1.5))
                elif time == "DAYTIME":
                    pop = int(base_pop * random.uniform(0.8, 1.1))
                else: # NIGHTTIME
                    pop = int(base_pop * random.uniform(0.9, 1.3))
                    
                data.append({
                    "dong_code": dong["code"],
                    "dong_name": dong["name"],
                    "day_type": day,
                    "time_slot": time,
                    "avg_population": pop
                })
                
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(DATASET_DIR, "population_density.csv"), index=False, encoding="utf-8-sig")

def generate_safety_infra():
    """5. 안전 인프라(CCTV 및 가로등) 모의 데이터 생성 (safety_infra.csv)"""
    print("Generating Mock Safety Infra...")
    
    # CCTV 생성 (60개)
    cctv_coords = generate_random_coords(60)
    data = []
    for i, (lat, lng) in enumerate(cctv_coords):
        dong = random.choice(DONG_LIST)
        data.append({
            "infra_id": f"CC_{5000 + i}",
            "type": "CCTV",
            "sig_cd": "11620",
            "dong_code": dong["code"],
            "latitude": lat,
            "longitude": lng,
            "status": "ACTIVE"
        })
        
    # 가로등 생성 (120개)
    lamp_coords = generate_random_coords(120)
    for i, (lat, lng) in enumerate(lamp_coords):
        dong = random.choice(DONG_LIST)
        data.append({
            "infra_id": f"LP_{6000 + i}",
            "type": "STREETLAMP",
            "sig_cd": "11620",
            "dong_code": dong["code"],
            "latitude": lat,
            "longitude": lng,
            "status": "ACTIVE"
        })
        
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(DATASET_DIR, "safety_infra.csv"), index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    print(f"Dataset target path: {DATASET_DIR}")
    generate_nosmoking_zones()
    generate_kindergartens()
    generate_transit_data()
    generate_population_density()
    generate_safety_infra()
    print("Mock Data Generation Successfully Completed!")
