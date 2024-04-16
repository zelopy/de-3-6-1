# import requests
# import json

# key = '5056614767646f6f31313458426f7672'
# start = 1
# end = 1000
# cnt = 0
# ress = []

# while True:
#     cnt+=1
#     url = f'http://openapi.seoul.go.kr:8088/%7Bkey%7D/json/bikeList/%7Bstart%7D/%7Bend%7D/'
#     res = requests.get(url).json()

#     try:
#         res1 = res['rentBikeStatus']['row']
#         ress += res1
#         if res['rentBikeStatus']['RESULT']['CODE'] == 'INFO-200':
#             break
#     except KeyError:
#         print("No rentBikeStatus in data. Exiting loop.")
#         break

#     start += 1000
#     end += 1000

# # print(len(ress))
# ress= pd.DataFrame(ress)

# ress['rackTotCnt'] = ress['rackTotCnt'].astype(int)
# ress['stationName'] = ress['stationName'].astype(str)
# ress['parkingBikeTotCnt'] = ress['parkingBikeTotCnt'].astype(int)
# ress['shared'] = ress['shared'].astype(int)
# ress['stationLatitude'] = ress['stationLatitude'].astype(float)
# ress['stationLongitude'] = ress['stationLongitude'].astype(float)
# ress['stationId'] = ress['stationId'].astype(str)

# # ress.info()