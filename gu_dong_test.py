res1 = requests.get('http://openapi.seoul.go.kr:8088/576f445751686a6a3636776952594f/json/bikeList/1/1000/')
res2 = requests.get('http://openapi.seoul.go.kr:8088/576f445751686a6a3636776952594f/json/bikeList/1001/2000/')
res3 = requests.get('http://openapi.seoul.go.kr:8088/576f445751686a6a3636776952594f/json/bikeList/2001/2697/')
items = []
items.extend(json.loads(res1.text)['rentBikeStatus']['row'])
items.extend(json.loads(res2.text)['rentBikeStatus']['row'])
items.extend(json.loads(res3.text)['rentBikeStatus']['row'])


# 정거장 정보 중 몇개는 위치 정보를 찾을 수 없음
# 현재 총 데이터 중 14개의 구동데이터 빠짐
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
        if 'response' in data and 'result' in data['response'] and len(data['response']['result']) > 0:
            result = data['response']['result'][0]
            level2 = result['structure']['level2']
            level4 = result['structure']['level4L']
            if level4[-1] == "가":
                level4 = (level4+"동")
        else:
            print("No result found.:")
    else:
        print("Error:", response.status_code)
