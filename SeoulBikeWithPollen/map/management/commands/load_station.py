import json
from django.conf import settings
from django.core.management.base import BaseCommand
from map.models import Station
import requests
import csv
from map.serializers import LocationSerializer, StationSerializer

class Command(BaseCommand):
    help = 'Load data from Seoul Bike Station file'

    def handle(self, *args, **kwargs): 
        
        # 자전거 정거장 정보 불러와서 Station 모델에 저장
        res1 = requests.get('http://openapi.seoul.go.kr:8088/576f445751686a6a3636776952594f/json/bikeList/1/1000/')
        res2 = requests.get('http://openapi.seoul.go.kr:8088/576f445751686a6a3636776952594f/json/bikeList/1001/2000/')
        res3 = requests.get('http://openapi.seoul.go.kr:8088/576f445751686a6a3636776952594f/json/bikeList/2001/2697/')

        items = []
        items.extend(json.loads(res1.text)['rentBikeStatus']['row'])
        items.extend(json.loads(res2.text)['rentBikeStatus']['row'])
        items.extend(json.loads(res3.text)['rentBikeStatus']['row'])
        
        for item in items:
            serializer = StationSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
            else:
                self.stderr.write(f'Error occured while loading station : {serializer.errors}')


        # 지도를 나눌 행정동별 중심 좌표를 불러와서 행정동 별로 나누어서 Location 모델에 저장
        with open('map/data/location_center.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = row['코드']
                gu_name = row['시군구명']
                dong_name = row['읍면동명']
                longitude = float(row['X'])
                latitude = float(row['Y'])

                # LocationSerializer를 사용하여 데이터 직렬화
                serializer = LocationSerializer(data={
                    'code': code,
                    'guName': gu_name,
                    'dongName': dong_name,
                    'longitude': longitude,
                    'latitude': latitude
                })

                if serializer.is_valid():
                    # 유효한 경우, 데이터 저장
                    serializer.save()
                else:
                    # 유효하지 않은 경우, 에러 메시지 출력
                    self.stderr.write(f'Error occurred while loading data into Location model: {serializer.errors}')




        






