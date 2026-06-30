import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 타겟 디렉토리 지정 (사용자 데스크톱의 데이터셋 폴더)
DATASET_DIR = "C:\\Users\\Admin\\Desktop\\빅프로젝트 관련자료\\데이터셋"

def preprocess_transit_data():
    """
    가공 대상: 3번(정류소 위치 마스터) + 4번(버스 승하차 통계)
    가공 형태: 정류소별 위경도 좌표와 월평균 이용객 수가 결합된 단일 공간 데이터프레임
    """
    print("Preprocessing Transit (Bus) Data...")
    
    # 파일 경로
    pos_file = os.path.join(DATASET_DIR, "seoul_bus_passengers.json") # 승하차 샘플 (이전 단계 다운로드됨)
    
    if not os.path.exists(pos_file):
        print(f"Error: Required sample file not found at {pos_file}")
        return
        
    # 샘플 JSON 읽기
    with open(pos_file, 'r', encoding='utf-8') as f:
        df_passengers = pd.read_json(f)
    
    # 실제 OpenAPI 응답 구조인 CardBusTimeNew.row 추출
    if "CardBusTimeNew" in df_passengers.columns:
        rows = df_passengers["CardBusTimeNew"]["row"]
        df_passengers = pd.DataFrame(rows)
    
    print("Raw Passenger Data columns:", df_passengers.columns.tolist())
    
    # 텍스트 수치 데이터의 정수(Int) 가공
    # 서울시 버스/지하철 데이터의 승하차 인원 컬럼 수치 형변환
    # (일부 공공데이터는 숫자가 텍스트 형태로 제공되므로 전처리 필수)
    numeric_cols = [c for c in df_passengers.columns if '승차' in c or '하차' in c]
    for col in numeric_cols:
        df_passengers[col] = pd.to_numeric(df_passengers[col], errors='coerce').fillna(0).astype(int)
        
    # 총 승하차량 합계 계산
    df_passengers['total_volume'] = df_passengers[numeric_cols].sum(axis=1)
    
    # 정류소 기준 그룹바이 (요일/시간대 평균 산출 목적)
    df_grouped = df_passengers.groupby(['BUS_STA_NM', 'BUS_STA_NO'])['total_volume'].mean().reset_index()
    
    print("Preprocessed Transit Data (Sample):")
    print(df_grouped.head())
    
    # 향후 여기에 버스정류소 좌표 마스터(3번)를 BUS_STA_NO 기준으로 Merge함:
    # df_merged = pd.merge(df_grouped, df_coords, on='BUS_STA_NO', how='inner')
    # gpd.GeoDataFrame(df_merged, geometry=gpd.points_from_xy(df_merged.X좌표, df_merged.Y좌표), crs="EPSG:4326")
    
def preprocess_geojson_crs(shp_path, target_epsg=4326):
    """
    가공 대상: 6번(행정동 공간정보) 및 9번(연속지적도 SHP)
    가공 형태: 좌표계가 타겟 공간 좌표계(WGS84, EPSG:4326)로 투영 변환 완료된 공간 데이터
    """
    if not os.path.exists(shp_path):
        print(f"SHP file not found at {shp_path}")
        return
        
    print(f"Reading spatial file: {shp_path}")
    gdf = gpd.read_file(shp_path)
    
    print(f"Original CRS: {gdf.crs}")
    # 좌표계 투영 변환 가공
    gdf_transformed = gdf.to_crs(epsg=target_epsg)
    print(f"Transformed CRS to: {gdf_transformed.crs}")
    
    return gdf_transformed

if __name__ == "__main__":
    preprocess_transit_data()
