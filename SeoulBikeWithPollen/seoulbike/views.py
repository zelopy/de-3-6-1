from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404
import requests

# Create your views here.
def bike_station_info(request):
    gu_list = SeoulBikeStationNow.objects.values_list('station__addr1', flat=True).distinct()
    if request.method == 'POST':
        gu = request.POST.get('gu')
        dong = request.POST.get('dong')
        bike_stations = SeoulBikeStationNow.objects.filter(station__addr1=gu, station__addr2=dong)
        return render(request, 'bike_station_info.html', {'bike_stations': bike_stations})
    return render(request, 'bike_station_search.html', {'gu_list': gu_list})


def bike_station_info_by_gu_and_dong(request):
    gu_list = SeoulBikeStationNow.objects.values_list('station__addr1', flat=True).distinct()
    if request.method == 'POST':
        gu = request.POST.get('gu')
        dong = request.POST.get('dong')
        stations = SeoulBikeStationInfo.objects.get(pk="addr2")
        key = open("key.txt", 'r').read()
        # 구와 동이 모두 입력되었는지 확인
        if gu and dong:
            # API를 통해 해당 구와 동에 대한 따릉이 대여소 정보를 가져오기
            url = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/1/1000/'
            response = requests.get(url)
            
            if response.status_code == 200:
                bike_stations = response.json()["rentBikeStatus"]["row"]
                return render(request, 'bike_station_info.html', {'bike_stations': bike_stations})
            else:
                error_message = "따릉이 대여소 정보를 가져오는데 실패했습니다."
                return render(request, 'bike_station_search.html', {'gu_list': gu_list, 'error_message': error_message})
        
        # 구와 동이 모두 입력되지 않은 경우
        else:
            error_message = "구와 동을 모두 입력해주세요."
            return render(request, 'bike_station_search.html', {'gu_list': gu_list, 'error_message': error_message})
    
    # GET 요청일 경우
    return render(request, 'bike_station_search.html', {'gu_list': gu_list})