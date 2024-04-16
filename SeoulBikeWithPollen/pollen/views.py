from django.shortcuts import render
from rest_framework import serializers, generics, renderers
from .models import PollenAddrCode
from pollen.serializers import *
from .pollen_api_service import get_pollen_data
from rest_framework.response import Response

class PollenApiView(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = PollenAddrCodeSerializer
    
    # 행정구역코드 찾기
    def get_queryset(self):
        return PollenAddrCode.objects.filter(
            addr1=self.request.query_params.get('addr1', None),
            addr2=self.request.query_params.get('addr2', None),
            addr3=self.request.query_params.get('addr3', None)
            )
    
    def get(self, request, *args, **kwargs):
        print('PollenApiView.get() called')
        queryset = self.get_queryset()
        if queryset.exists():
            obj = queryset.first()
            addr_code = obj.addr_code

            result_pine = get_pollen_data('pine', addr_code)
            # result_weeds = get_pollen_data('weeds', addr_code)
            # result_oak = get_pollen_data('oak', addr_code)

            print(result_pine)
            # print(result_weeds)
            # print(result_oak)

            # TODO : JSON 병합? 아니면 타입별 구분 호출?

            return Response(result_pine)
        else:
            return Response({'error': '데이터가 없습니다.'})

