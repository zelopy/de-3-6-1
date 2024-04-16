from django.db import models
import requests

# Create your models here.
class BikeStation(models.Model):
    stationName = models.CharField(max_length=100)
    rackTotCnt = models.IntegerField()
    parkingBikeTotCnt = models.IntegerField()
    shared = models.IntegerField()
    stationLatitude = models.FloatField()
    stationLongitude = models.FloatField()
    stationId = models.CharField(max_length=100)

    @staticmethod
    def save_bike_data():
        key = '5056614767646f6f31313458426f7672'
        start = 1
        end = 1000
        cnt = 0
        while True:
            cnt += 1
            url = f'http://openapi.seoul.go.kr:8088/{{key}}/json/bikeList/{{start}}/{{end}}/'
            res = requests.get(url).json()
            try:
                res1 = res['rentBikeStatus']['row']
                for data in res1:
                    # BikeStation 모델에 데이터 저장
                    BikeStation.objects.create(
                        stationName=data["stationName"],
                        rackTotCnt=int(data["rackTotCnt"]),
                        parkingBikeTotCnt=int(data["parkingBikeTotCnt"]),
                        shared=int(data["shared"]),
                        stationLatitude=float(data["stationLatitude"]),
                        stationLongitude=float(data["stationLongitude"]),
                        stationId=data["stationId"]
                    )
                if res['rentBikeStatus']['RESULT']['CODE'] == 'INFO-200':
                    break
            except KeyError:
                print("No rentBikeStatus in data. Exiting loop.")
                break

            start += 1000
            end += 1000

        print("Data saved successfully.")