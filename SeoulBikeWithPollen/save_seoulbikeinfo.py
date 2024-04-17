# 전처리를 위한 프로그램
import requests
import geopandas as gpd
import pandas as pd

def save_seoulbikeinfo(key):
    """
    따릉이 대여소 전체 정보를 항상 request 하지 않도록 미리 대여소 정보를 파일로 저장하는 함수
    입력 : 서울열린데이터광장 키 값
    출력 : 없음. seoulbike.txt 파일이 저장됨
    """
    url1 = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/1/1000/'
    url2 = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/1001/2000/'
    url3 = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/2001/2694/'

    response1 = requests.get(url1).json()
    response2 = requests.get(url2).json()
    response3 = requests.get(url3).json()
    res1 = response1["rentBikeStatus"]["row"]
    res2 = response2["rentBikeStatus"]["row"]
    res3 = response3["rentBikeStatus"]["row"]
    ress = res1 + res2 + res3
    print(len(ress))
    # print(json.dumps(response, ensure_ascii=False, indent=3))
    # print(response["rentBikeStatus"]["row"][50]["stationName"])

    with open("seoulbikeinfo.txt", 'w', encoding='utf-8') as f:
        f.write("#station_id | station_name | raccnt | station_lat | station_lon\n9")
        for res in ress:
            raccnt = res["rackTotCnt"]
            name = res["stationName"]
            id = res["stationId"]
            stationlat = res["stationLatitude"][:-2]
            stationlon = res["stationLongitude"][:-2]
            f.write("%s | %s | %s | %s | %s\n" %(id, name, raccnt, stationlat, stationlon))


def latlon_to_gudong(seoulbikeinfo, shapefname, gudongfname):
    """
    save_seoulbikeinfo 함수로 생성된 seoulbikeinfo 파일과 동 경계 shapefile, 구별 동 정보가 포함된 csv 파일로
    따릉이 대여소 정보를 csv 파일로 만들어주는 함수
    input : 
    seoulbikeinfo : save_seoulbikeinfo로 생성된 파일이름
    shapefname : shape파일 이름
    gudongfname : 구별 동 정보 csv파일 이름
    output : 없음. seoulbikeinfo.csv 파일 생성
    """
    names = ["station_id", "station_name", "raccnt", "station_lat", "station_lon"]
    bike = pd.read_csv(seoulbikeinfo, sep='|', names=names, encoding='utf-8', header=0)
    gdf_bike = gpd.GeoDataFrame(bike, geometry=gpd.points_from_xy(bike["station_lon"], bike["station_lat"]), crs='WGS84')

    gdf_dong = gpd.read_file(shapefname, encoding='cp949')
    gdf_bike_dong = gpd.sjoin(gdf_bike.to_crs("epsg:5186"), gdf_dong)
    gdf_bike_dong = gdf_bike_dong.drop(['geometry', 'index_right', 'BASE_DATE', 'ADM_CD'], axis = 1)

    names = ['gu', 'num', 'ADM_NM']
    gudong = pd.read_csv(gudongfname, sep='\t', names=names)
    gudong = gudong.drop('num', axis = 1)
    gdf_bike_dong = pd.merge(left=gdf_bike_dong, right=gudong, how='inner', on="ADM_NM")

    gdf_bike_dong.to_csv('seoulblikeinfo3.csv', sep=',')


if __name__ == "__main__":
    key = open("key.txt", 'r').read()
    save_seoulbikeinfo(key)
    latlon_to_gudong("seoulbikeinfo.txt", '../DONG_PG.shp', "../guanddong.txt")