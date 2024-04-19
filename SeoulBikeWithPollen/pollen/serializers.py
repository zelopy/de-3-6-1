from rest_framework import serializers
from .models import PollenAddrCode, PollenApi

class PollenAddrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollenAddrCode
        fields = ['addr_code', 'addr1', 'addr2', 'addr3']

class PollenApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollenApi
        fields = ['code', 'areaNo', 'date', 'today', 'tomorrow', 'dayaftertomorrow', 'twodaysaftertomorrow']