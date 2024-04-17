import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from shapely.geometry import Point, Polygon, LineString
import geopandas as gpd
import pandas as pd
from pyproj import Transformer
import pyproj
import numpy as np
import folium
import os
import sqlite3

print(os.getcwd())
df = pd.read_csv('seoulblikeinfo.csv', sep=',')
df = df.rename(columns={"station_lat":"latitude", "station_lon":"longitude", "ADM_NM":"addr2","gu":"addr1"}).drop(df.columns[0], axis=1)

for i in df.iterrows():
    print(i[0])

# print(df)
# conn = sqlite3.connect('db.sqlite3')
# df.to_sql('seoulbike_SeoulBikeStationInfo', conn, if_exists="replace", index=False)
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM seoulbike_seoulbikestationinfo WHERE addr2='연희동';")
# # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())


"""
names = ["station_id", "station_name", "raccnt", "station_lat", "station_lon"]
bike = pd.read_csv("seoulbikeinfo.txt", sep='|', names=names, encoding='utf-8', header=0)

gdf_bike = gpd.GeoDataFrame(bike, geometry=gpd.points_from_xy(bike["station_lon"], bike["station_lat"]), crs='WGS84')

gdf_dong = gpd.read_file('../DONG_PG.shp', encoding='cp949')
gdf_bike_dong = gpd.sjoin(gdf_bike.to_crs("epsg:5186"), gdf_dong)
gdf_bike_dong = gdf_bike_dong.drop(['geometry', 'index_right', 'BASE_DATE', 'ADM_CD'], axis = 1)

names = ['gu', 'num', 'ADM_NM']
gudong = pd.read_csv("../guanddong.txt", sep='\t', names=names)
gudong = gudong.drop('num', axis = 1)
gdf_bike_dong = pd.merge(left=gdf_bike_dong, right=gudong, how='inner', on="ADM_NM")

gdf_bike_dong.to_csv('seoulblikeinfo.csv', sep=',')

# 기본 정보 가져오기
key = open("key.txt", 'r').read()
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
        try:
            id, name = res["stationName"].split(". ")
        except ValueError:
            id = res["stationName"].split(".")[0]
            name = ".".join(res["stationName"].split(".")[1:])
        stationlat = res["stationLatitude"][:-2]
        stationlon = res["stationLongitude"][:-2]
        f.write("%s | %s | %s | %s | %s\n" %(id, name, raccnt, stationlat, stationlon))

raccnts = []
bikecnts = []
ratios = []
stationids = []
stationnames = []
stationlats = []
stationlons = []

for res in ress:
    raccnts.append(res["rackTotCnt"])
    bikecnts.append(res["parkingBikeTotCnt"])
    ratios.append(res["shared"])
    try:
        id, name = res["stationName"].split(". ")
    except ValueError:
        id = res["stationName"].split(".")[0]
        name = ".".join(res["stationName"].split(".")[1:])
    stationids.append(id)
    stationnames.append(name)
    stationlats.append(res["stationLatitude"][:-2])
    stationlons.append(res["stationLongitude"][:-2])

print(raccnts[3])
id, name = response1["rentBikeStatus"]["row"][0]["stationName"].split(". ")
print(id, name)

lat = response["rentBikeStatus"]["row"][0]["stationLatitude"][:-2]
lon = response["rentBikeStatus"]["row"][0]["stationLongitude"][:-2]
mapurl = f"http://map.kakao.com/link/map/{lat},{lon}"

res = requests.get(f"https://map.kakao.com/", verify=False, timeout=3)
soup = BeautifulSoup(res.text, "html.parser")
results = soup.find("a", id='localInfo.map.town')

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get(mapurl)
    time.sleep(1)
    result = driver.find_element(By.ID, "localInfo.map.town")
    print(result.text)

"""