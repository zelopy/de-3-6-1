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

# gdf_admin_gu_pg = gpd.read_file('SeoulBikeWithPollen\dong_pg\BND_ADM_DONG_PG.shp', encoding='cp949')  
# print(gdf_admin_gu_pg.head())

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

# print(raccnts[3])
# id, name = response1["rentBikeStatus"]["row"][0]["stationName"].split(". ")
# print(id, name)

# lat = response["rentBikeStatus"]["row"][0]["stationLatitude"][:-2]
# lon = response["rentBikeStatus"]["row"][0]["stationLongitude"][:-2]
# mapurl = f"http://map.kakao.com/link/map/{lat},{lon}"

# res = requests.get(f"https://map.kakao.com/", verify=False, timeout=3)
# soup = BeautifulSoup(res.text, "html.parser")
# results = soup.find("a", id='localInfo.map.town')

# with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
#     driver.get(mapurl)
#     time.sleep(1)
#     result = driver.find_element(By.ID, "localInfo.map.town")
#     print(result.text)

