import re

res1 = requests.get('http://openapi.seoul.go.kr:8088/576f445751686a6a3636776952594f/json/bikeList/1/100/')


items = []
items.extend(json.loads(res1.text)['rentBikeStatus']['row'])


# 정거장 정보 중 몇개는 위치 정보를 찾을 수 없음
# 현재 총 데이터 중 14개의 구동데이터 빠짐,  동 이름이..ㅜ
for i in items:
    apiurl = "https://api.vworld.kr/req/address?"
    params = {
        "service": "address",
        "request": "getaddress",
        "crs": "epsg:4326",
        "point": f"{i['stationLongitude']},{i['stationLatitude']}",
        "format": "json",
        "type": "PARCEL",
        "key": "660CBAC5-AA5D-369E-82E3-3FF91B377482"
    }
    response = requests.get(apiurl, params=params)
    if response.status_code == 200:
        data = response.json()
#         print(data)
        if 'response' in data and 'result' in data['response'] and len(data['response']['result']) > 0:
            result = data['response']['result'][0]
            level2 = result['structure']['level2']
            if 'level4A' in result['structure'] and result['structure']['level4A']:
                level4 = result['structure']['level4A']
                level4 = re.sub(r'제(\d)', r'\1', level4)

            else:
                level4 = result['structure']['level4L']

#             print(level4)
            if level4[-1] == "가":
                level4 = (level4+"동")
        else:
            # 위치 정보 없는 코드 임의로 설정
#             print("No result found.:")
            level2 = "종로구"
            level4 = "사직동"

        # add2 = 구 / add3 = 동
        i['addr2'] = level2
        i['addr3'] = level4 
    else:
        print("Error:", response.status_code)
