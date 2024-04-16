from django.shortcuts import render
from rest_framework import serializers, generics, renderers
from .models import PollenAddrCode
from pollen.serializers import *
from .pollen_api_service import get_pollen_data
from rest_framework.response import Response
import json
from django.http import JsonResponse

class PollenInputView(generics.GenericAPIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        dummy_data = [
            {'addr2': '성동구', 'addr3': [
                {'name': '행당제1동', 'addr_code': '1120056000'},
                {'name': '행당제2동', 'addr_code': '1120056001'},
                {'name': '응봉동', 'addr_code': '1120056002'},
                {'name': '금호1가동', 'addr_code': '1120056003'},
                {'name': '금호2.3가동', 'addr_code': '1120056004'}
            ]},
            {'addr2': '광진구', 'addr3': [
                {'name': '군자동', 'addr_code': '1121573000'},
                {'name': '중곡제1동', 'addr_code': '1121574000'},
                {'name': '중곡제2동', 'addr_code': '1121575000'},
                {'name': '중곡제3동', 'addr_code': '1121576000'},
                {'name': '중곡제4동', 'addr_code': '1121577000'}
            ]},
            {'addr2': '송파구', 'addr3': [
                {'name': '거여1동', 'addr_code': '1171053100'},
                {'name': '거여2동', 'addr_code': '1171053200'},
                {'name': '마천1동', 'addr_code': '1171054000'},
                {'name': '마천2동', 'addr_code': '1171055000'},
                {'name': '방이1동', 'addr_code': '1171056100'}
            ]}
        ]
         
        return render(request, 'input.html', {'addr_data': dummy_data})
    
    def post(self, request, *args, **kwargs):
        addr2 = request.data.get('addr2')
        addr3 = request.data.get('addr3')
        
        return JsonResponse({
            'addr2': addr2,
            'addr3': addr3
        })


class PollenApiView(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = PollenAddrCodeSerializer
    
    # 행정구역코드 찾기
    def get_queryset(self):
        return PollenAddrCode.objects.filter(
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
    

