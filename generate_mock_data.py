import os
import csv
import random

# 데이터 저장 디렉토리 생성
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

# 마포구 중심 영역 위경도 바운딩 박스 설정 (대략적인 마포구 범위)
LAT_MIN, LAT_MAX = 37.5450, 37.5680
LNG_MIN, LNG_MAX = 126.9000, 126.9400

def generate_mock_nosmoking(count=50):
    """
    모의 금연구역 데이터 생성 (CSV)
    필수 컬럼: 금연구역명, 도로명주소, 위도, 경도, 금연구역면적
    """
    filepath = os.path.join(DATA_DIR, "mapo_nosmoking.csv")
    names = ["대흥동 공원", "상암동 빌딩 앞", "신촌역 이면도로", "합정역 광장", "공덕역 빌딩 뒤편", "망원시장 입구"]
    
    with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["금연구역명", "도로명주소", "위도", "경도", "금연구역면적"])
        
        for i in range(count):
            lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
            lng = round(random.uniform(LNG_MIN, LNG_MAX), 6)
            name = f"{random.choice(names)} {random.randint(1, 100)}"
            area = random.randint(10, 500)
            addr = f"서울특별시 마포구 백범로 {random.randint(1, 300)}길"
            writer.writerow([name, addr, lat, lng, area])
            
    print(f"Generated nosmoking data: {filepath} ({count} rows)")

def generate_mock_kindergarten(count=30):
    """
    모의 어린이집 데이터 생성 (CSV)
    필수 컬럼: 어린이집명, 어린이집유형구분, 위도, 경도, 정원수
    """
    filepath = os.path.join(DATA_DIR, "mapo_kindergarten.csv")
    names = ["마포 구립 어린이집", "새싹 어린이집", "꿈나무 어린이집", "상암 스마트 어린이집", "공덕 햇살 어린이집"]
    types = ["국공립", "민간", "가정", "사회복지법인"]
    
    with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["어린이집명", "어린이집유형구분", "위도", "경도", "정원수"])
        
        for i in range(count):
            lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
            lng = round(random.uniform(LNG_MIN, LNG_MAX), 6)
            name = f"{random.choice(names)} {random.randint(1, 20)}"
            k_type = random.choice(types)
            capacity = random.randint(15, 120)
            writer.writerow([name, k_type, lat, lng, capacity])
            
    print(f"Generated kindergarten data: {filepath} ({count} rows)")

def generate_mock_bus_stations(count=80):
    """
    모의 버스정류장 및 이용객 데이터 생성 (CSV)
    필수 컬럼: 정류소명, 정류소번호, 위도, 경도, 월평균이용객수
    """
    filepath = os.path.join(DATA_DIR, "mapo_bus_stations.csv")
    names = ["마포역", "신촌역", "이대역", "합정역", "홍대입구역", "대흥역", "망원역", "서강대역", "마포구청역"]
    
    with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["정류소명", "정류소번호", "위도", "경도", "월평균이용객수"])
        
        for i in range(count):
            lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
            lng = round(random.uniform(LNG_MIN, LNG_MAX), 6)
            station_id = f"14{random.randint(100, 999):03d}"
            name = f"{random.choice(names)} 정류장 {random.randint(1, 5)}"
            passengers = random.randint(1000, 150000)
            writer.writerow([name, station_id, lat, lng, passengers])
            
    print(f"Generated bus stations data: {filepath} ({count} rows)")

def generate_mock_cctv(count=60):
    """
    모의 CCTV 위치 데이터 생성 (CSV)
    필수 컬럼: 관리번호, 위도, 경도
    """
    filepath = os.path.join(DATA_DIR, "mapo_cctv.csv")
    
    with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["관리번호", "위도", "경도"])
        
        for i in range(count):
            lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
            lng = round(random.uniform(LNG_MIN, LNG_MAX), 6)
            cctv_id = f"MP-CCTV-{i:04d}"
            writer.writerow([cctv_id, lat, lng])
            
    print(f"Generated CCTV data: {filepath} ({count} rows)")

if __name__ == "__main__":
    print("Starting mock data generation for Mapo-gu using Standard Library...")
    generate_mock_nosmoking()
    generate_mock_kindergarten()
    generate_mock_bus_stations()
    generate_mock_cctv()
    print("All mock datasets generated successfully in ./data directory.")
