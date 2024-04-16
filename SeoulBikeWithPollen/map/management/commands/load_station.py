import json
from django.conf import settings
from django.core.management.base import BaseCommand
from map.models import Station
import requests
from map.serializers import StationSerializer

class Command(BaseCommand):
    help = 'Load data from Seoul Bike Station file'

    def handle(self, *args, **kwargs): 

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






        






