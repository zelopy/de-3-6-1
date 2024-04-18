from rest_framework import serializers
from .models import Station, Location


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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['code', 'guName', 'dongName', 'longitude', 'latitude']