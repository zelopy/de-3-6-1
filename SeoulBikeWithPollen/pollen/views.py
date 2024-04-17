from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, generics, renderers
from .models import PollenAddrCode
from pollen.serializers import *
from .pollen_api_service import get_pollen_data, addr_code_list
from rest_framework.response import Response
from django.http import JsonResponse

class PollenApiView(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = PollenAddrCodeSerializer
    
    def get(self, request):
        # print('PollenApiView.get() called')
        pollen_type = self.request.query_params.get('pollen_type', None)
        area_no = self.request.query_params.get('area_no', None)

        result = get_pollen_data(pollen_type, area_no)
        # print(result['response']['body']['items']['item'])

        return Response(result['response']['body']['items']['item'][0])

'''
행정구역코드 목록 조회
'''
def result(request, addr2=None):
    # print(f'result() addr2:{addr2}')
    if addr2 is None:
        addr2 = ''
    addr_list = addr_code_list(addr2)
    return JsonResponse({'addr_list': addr_list})
