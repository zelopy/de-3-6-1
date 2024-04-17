from .models import *
from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect



def bike_station_info(request):
    gu_list = SeoulBikeStationInfo.objects.values_list('addr1', flat=True).distinct()

    if request.method == 'POST' and 'gu' in request.POST and 'dong' in request.POST:
        selected_gu = request.POST.get('gu')
        selected_dong = request.POST.get('dong')
        return HttpResponseRedirect(reverse('seoulbike:now', args=(selected_gu,selected_dong)))    
    
    if request.method == 'POST':
        gu = request.POST.get('gu')
        dong_list = SeoulBikeStationInfo.objects.filter(addr1=gu).values_list('addr2', flat=True).distinct()
        return JsonResponse({'dong_list': list(dong_list)})

    return render(request, 'seoulbike/bike_station_search.html', {'gu_list': gu_list})


def bike_station_now(request, addr1, addr2):
    stations = SeoulBikeStationInfo.objects.filter(addr2 = addr2)
    ids = []
    for station in stations:
        ids.append(station.id)
    nows = {}
    key = open("key.txt", 'r').read()
    try:
        if max(ids) - min(ids) < 900:
            url = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/{min(ids)-10}/{max(ids)+10}/'
            response = requests.get(url).json()
            stations = response1["rentBikeStatus"]["row"]
        else:
            url1 = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/1/1000/'
            url2 = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/1001/2000/'
            url3 = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/2001/2694/'
            response1 = requests.get(url1).json()
            response2 = requests.get(url2).json()
            response3 = requests.get(url3).json()
            res1 = response1["rentBikeStatus"]["row"]
            res2 = response2["rentBikeStatus"]["row"]
            res3 = response3["rentBikeStatus"]["row"]
            stations = res1 + res2 + res3

        for station in stations:
            if station['stationId'] in ids:
                
                
        filtered_bike_stations = [station for station in stations if station['stationLatitude'] == addr1 and station['addr2'] == addr2]
        return render(request, 'seoulbike/bike_station_now.html', {'bike_stations': filtered_bike_stations})
    except:
        error_message = "API 요청에 실패했습니다."
        return render(request, 'seoulbike/error.html', {'error_message': error_message})
    

        

# def bike_station_now(request):
#     gu_list = SeoulBikeStationNow.objects.values_list('station__addr1', flat=True).distinct()
#     if request.method == 'POST':
#         gu = request.POST.get('gu')
#         dong = request.POST.get('dong')
#         stations = SeoulBikeStationInfo.objects.filter(addr2 = dong)
#         key = open("key.txt", 'r').read()
#         # 구와 동이 모두 입력되었는지 확인
#         if gu and dong:
#             # API를 통해 해당 구와 동에 대한 따릉이 대여소 정보를 가져오기
#             url = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/1/1000/'
#             response = requests.get(url)
            
#             if response.status_code == 200:
#                 bike_stations = response.json()["rentBikeStatus"]["row"]
#                 return render(request, 'bike_station_info.html', {'bike_stations': bike_stations})
#             else:
#                 error_message = "따릉이 대여소 정보를 가져오는데 실패했습니다."
#                 return render(request, 'bike_station_search.html', {'gu_list': gu_list, 'error_message': error_message})
        
#         # 구와 동이 모두 입력되지 않은 경우
#         else:
#             error_message = "구와 동을 모두 입력해주세요."
#             return render(request, 'bike_station_search.html', {'gu_list': gu_list, 'error_message': error_message})
    
#     # GET 요청일 경우
#     return render(request, 'bike_station_search.html', {'gu_list': gu_list})