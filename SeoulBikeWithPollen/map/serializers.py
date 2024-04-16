from rest_framework import serializers
from .models import Station

class StationSerializer(serializers.ModelSerializer):
    rackTotCnt = serializers.IntegerField()
    stationName = serializers.CharField()
    parkingBikeTotCnt = serializers.IntegerField()
    shared = serializers.IntegerField()
    stationLatitude = serializers.FloatField()
    stationLongitude = serializers.FloatField()
    stationId = serializers.CharField()

    class Meta:
        model = Station
        fields = ['rackTotCnt', 'stationName', 'parkingBikeTotCnt', 'shared', 'stationLatitude', 'stationLongitude', 'stationId']