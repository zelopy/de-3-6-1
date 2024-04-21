from django.shortcuts import render
from rest_framework import generics, renderers
from pollen.serializers import *
from .pollen_api_service import get_pollen_data, addr_code_list
from rest_framework.response import Response

class PollenApiView(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = PollenAddrCodeSerializer
    
    def get(self, request):
        pollen_type = self.request.query_params.get('pollen_type', None)
        area_no = self.request.query_params.get('area_no', None)

        result = get_pollen_data(pollen_type, area_no)

        pollen_data = result['response']['body']['items']['item'][0]

        # 현재시간이 18시 이후라면 today가 비어있기 때문에 하루씩 앞당겨서 조정
        if pollen_data['today'] == '':
            pollen_data['today'], pollen_data['tomorrow'], pollen_data['dayaftertomorrow'] = pollen_data['tomorrow'], pollen_data['dayaftertomorrow'], pollen_data['twodaysaftertomorrow']

        return Response(pollen_data)

def index(request,addr2=None):
        if addr2 is None:
            addr2 = ''
        addr_data = addr_code_list(addr2)
        context = {'addr_data': addr_data}
        return render(request, 'input.html', context)