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

    # 행정구역코드 찾기

    
    def get(self, request, *args, **kwargs):
        print('PollenApiView.get() called')
        
        addr_code = self.request.query_params.get('area_no')
        pollen_type = self.request.query_params.get('pollen_type', 'pine')  # 꽃가루 타입 기본값은 'pine'입니다.
        

        result_pine = get_pollen_data(pollen_type, addr_code)
        # result_weeds = get_pollen_data('weeds', addr_code)
        # result_oak = get_pollen_data('oak', addr_code)

        print(result_pine)
        # print(result_weeds)
        # print(result_oak)

        # TODO: JSON 병합? 아니면 타입별 구분 호출?

        return Response(result_pine)

def index(request,addr2=None):
        if addr2 is None:
            addr2 = ''
        addr_data = addr_code_list(addr2)
        context = {'addr_data': addr_data}
        return render(request, 'input.html', context)