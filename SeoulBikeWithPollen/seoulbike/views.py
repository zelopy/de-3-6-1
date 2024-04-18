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
    pks = []
    ids = []
    for station in stations:
        pks.append(int(station.id))
        ids.append(station.station_id)
    nows = []
    key = open("key.txt", 'r').read()
    try:
        if max(pks) - min(pks) < 900:
            url = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/{min(pks)-10}/{max(pks)+10}/'
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
                nows.append({"station_id":station["stationId"],"station_name":station["stationName"], "bikecnt":station["parkingBikeTotCnt"], "bikeratio":station["shared"]})
    except requests.exceptions.RequestException as e:
        error_message = "API 요청 중 오류가 발생했습니다."
        return render(request, 'seoulbike/error.html', {'error_message': error_message})

    return render(request, 'seoulbike/bike_station_now.html', {'nows': nows})