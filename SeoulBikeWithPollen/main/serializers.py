from rest_framework import serializers
from .models import SeoulBikeStationInfo, SeoulBikeStationNow

class SeoulBikeStationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulBikeStationInfo
        fields = ['station_id', 'station_name', 'raccnt', 'addr1', 'addr2', 'latitude', 'longitude']

class SeoulBikeStationNowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulBikeStationNow
        fields = ['station', 'bikecnt', 'bikeratio']