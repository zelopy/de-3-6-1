import requests
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

def get_api_data():
    key = '5056614767646f6f31313458426f7672'
    start = 1
    end = 1000
    cnt = 0
    ress = []

    while True:
        cnt += 1
        url = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/{start}/{end}/'
        res = requests.get(url).json()

        try:
            res1 = res['rentBikeStatus']['row']
            ress += res1
            if res['rentBikeStatus']['RESULT']['CODE'] == 'INFO-200':
                break
        except KeyError:
            print("No rentBikeStatus in data. Exiting loop.")
            break

        start += 1000
        end += 1000

    return res, ress

api_data, api_dict = get_api_data()

def index(request):
    gu_list = SeoulBikeStationInfo.objects.values_list('addr1', flat=True).distinct()

    if request.method == 'POST' and 'gu' in request.POST and 'dong' in request.POST:
        selected_gu = request.POST.get('gu')
        selected_dong = request.POST.get('dong')    
        return HttpResponseRedirect(reverse('now', args=(selected_gu,selected_dong)))    
    
    if request.method == 'POST':
        gu = request.POST.get('gu')
        dong_list = SeoulBikeStationInfo.objects.filter(addr1=gu).values_list('addr2', flat=True).distinct()
        return JsonResponse({'dong_list': list(dong_list)})

    return render(request, 'index.html', {'gu_list': gu_list})

def index_now(request, addr1, addr2):
    stations = SeoulBikeStationInfo.objects.filter(addr2 = addr2)
    pks = []
    ids = []
    for station in stations:
        pks.append(int(station.id))
        ids.append(station.station_id)
    nows = []
    key = '5056614767646f6f31313458426f7672'
    # try:
    if max(pks) - min(pks) < 900:
        url = f'http://openapi.seoul.go.kr:8088/{key}/json/bikeList/{min(pks)-10}/{max(pks)+10}/'
        response = requests.get(url).json()
        stations = response["rentBikeStatus"]["row"]
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
    return render(request, 'index.html', {'nows': nows})


# 아래 코드는 html 불러오기 용도
def kakaomap(request):
    api_data, api_dict = get_api_data()
    return render(request, 'kakaomap/map.html', {'api_data': api_data, 'api_dict': api_dict})

def header(request):
    return render(request, 'header.html')

def sidebar(request):
    return render(request,'sidebar.html')

def svgT1(request):
    return render(request,'svgT1.html')
def svgT2(request):
    return render(request,'svgT2.html')

@api_view()
def home(request):
    api_data, api_dict = get_api_data()
    return JsonResponse(api_dict, safe=False)
