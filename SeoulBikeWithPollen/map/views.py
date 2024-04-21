from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster
from map.models import Location, Station
import requests
from pollen.pollen_api_service import get_pollen_data

# 

# Create your views here.
def map(request):
    stations = Station.objects.all()
    locations = Location.objects.all()
    # gu_names = Location.objects.values_list('guName', flat=True).distinct().order_by('guName')
    
    # gu_dong_mapping = {}
    # for gu_name in gu_names:
    #     dong_names = Location.objects.filter(guName = gu_name).values_list('dongName', flat = True).distinct().order_by('dongName')
    #     gu_dong_mapping[gu_name] = list(dong_names)

    # 기본 지도
    # 쿼리 문자열 예시 : http://127.0.0.1:8000/map/?addr2=강남구&addr3=역삼1동
    if request.method == 'GET':

        gu_name = request.GET.get('addr2')
        dong_name = request.GET.get('addr3')
        pine_level = request.GET.get('pine_level')
        oak_level = request.GET.get('oak_level')
        
        def convert_to_gauge_bar(level):
            colors = {
                '회색': '#F2F2F2',
                '초록색': '#A5DF00',
                '노란색': '#F9F269',
                '주황색': '#FF8000',
                '빨간색': '#DF0101'
            }
            
            levels = {
                '낮음': '초록색 회색 회색 회색',
                '보통': '노란색 노란색 회색 회색',
                '높음': '주황색 주황색 주황색 회색',
                '매우 높음': '빨간색 빨간색 빨간색 빨간색'
            }
            
            bars = levels.get(level, '회색 회색 회색 회색').split()
            
            gauge_bars = ''.join([f'<div style="background-color: {colors.get(bar, "gray")}; width: 11%; height: 7px; margin-right: 0.7%; display: inline-block; border-radius: 4px;"></div>' 
 for bar in bars])
            
            return gauge_bars

        pine_gauge = convert_to_gauge_bar(pine_level)
        oak_gauge = convert_to_gauge_bar(oak_level)
        

        # 초기 지도 (구,동 입력이 없을 때)
        if gu_name is None and dong_name is None:
            initial_location = [37.5664056,126.9778222]
            
            m = folium.Map(location = initial_location,
                        control_scale = True,
                        zoom_start= 12, 
                        width = "100%", 
                        height = "100%")
            
            # MarkerCluster 이용해서 커스텀 마커 생성
            mCluster = MarkerCluster(name = "Markers Example").add_to(m)

            for station in stations:
                coordinate = (station.stationLatitude, station.stationLongitude)
            

                # 정거장 클릭 시 나타낼 정보 표시
                popup_content = (
                    f'<div style="margin-right: 20px;">'
                        f"<h4><b>{station.stationName}</b></h4>"
                        f"<h5>현재 대여 가능한 자전거 수 : {station.parkingBikeTotCnt}</h5>"
                        "<hr style='border-top: 2px solid #F2F2F2; margin: 10px 0;'>"
                        "<h4><b>꽃가루 농도</b></h4>"
                        f"<h5>소나무 : {pine_level}  {pine_gauge}</h5>"
                        f"<h5>참나무 : {oak_level}  {oak_gauge}</h5>"
                    f'</div>'
                )
        
                iframe = folium.IFrame(popup_content)
                popup = folium.Popup(iframe, min_width=280, max_width=400, min_height=500, max_height=600)
                
                
                
                if station.parkingBikeTotCnt == 0:
                    folium.Marker(coordinate, popup = popup, icon = folium.Icon(color = 'red', icon='bicycle', prefix='fa')).add_to(mCluster)
                    continue
                folium.Marker(coordinate, popup = popup, icon = folium.Icon(color = 'green', icon='bicycle', prefix='fa')).add_to(mCluster)

            folium.LayerControl().add_to(m)

            map_html = m._repr_html_()
            return HttpResponse(map_html)

            # context = {'map': m._repr_html_()}
            # return render(request, "pollenbike.html", context)
        
        # 쿼리 문자열로 구와 동 입력 시 실행
        else:
            latitude = Location.objects.get(guName = gu_name, dongName = dong_name).latitude
            longitude = Location.objects.get(guName = gu_name, dongName = dong_name).longitude

            m = folium.Map(location = [latitude, longitude],
                control_scale = True,
                zoom_start= 16, 
                width = "100%", 
                height = "100%")
        
            mCluster = MarkerCluster(name = "Markers Example").add_to(m)

            for station in stations:
                coordinate = (station.stationLatitude, station.stationLongitude)

                # 정거장 클릭 시 나타낼 정보 표시
                popup_content = (
                    f'<div style="margin-right: 20px;">'
                        f"<h4><b>{station.stationName}</b></h4>"
                        f"<h5>현재 대여 가능한 자전거 수 : {station.parkingBikeTotCnt}</h5>"
                        "<hr style='border-top: 2px solid #F2F2F2; margin: 10px 0;'>"
                        "<h4><b>꽃가루 농도</b></h4>"
                        f"<h5>소나무 : {pine_level}  {pine_gauge}</h5>"
                        f"<h5>참나무 : {oak_level}  {oak_gauge}</h5>"
                    f'</div>'
                )
        
                iframe = folium.IFrame(popup_content)
                popup = folium.Popup(iframe, min_width=280, max_width=400, min_height=500, max_height=600)

                
                
                if station.parkingBikeTotCnt == 0:
                    folium.Marker(coordinate, popup = popup, icon = folium.Icon(color = 'red', icon='bicycle', prefix='fa')).add_to(mCluster)
                    continue
                folium.Marker(coordinate, popup = popup, icon = folium.Icon(color = 'green', icon='bicycle', prefix='fa')).add_to(mCluster)

            folium.LayerControl().add_to(m)

            map_html = m._repr_html_()
            return HttpResponse(map_html)
        
            # context = {'map': m._repr_html_()}
            # return render(request, "pollenbike.html", context)


    # if request.method == 'POST':
    #     gu_name = request.POST.get('gu_name')
    #     dong_name = request.POST.get('dong_name')
    #     latitude = Location.objects.get(guName = gu_name, dongName = dong_name).latitude
    #     longitude = Location.objects.get(guName = gu_name, dongName = dong_name).longitude

    #     m = folium.Map(location = [latitude, longitude],
    #             control_scale = True,
    #             zoom_start= 16, 
    #             width = 1000, 
    #             height = 800)
        
    #     mCluster = MarkerCluster(name = "Markers Example").add_to(m)

    #     for station in stations:
    #         coordinate = (station.stationLatitude, station.stationLongitude)

    #         # 정거장 클릭 시 나타낼 정보 표시
    #         iframe = folium.IFrame('<b>' + station.stationName + '</b><br>' + '현재 대여 가능 : ' + str(station.parkingBikeTotCnt))
    #         popup = folium.Popup(iframe, min_width = 250, max_width = 250, min_height = 135, max_height = 135)
            
            
    #         if station.parkingBikeTotCnt == 0:
    #             folium.Marker(coordinate, popup = popup, icon = folium.Icon(color = 'red', icon='bicycle', prefix='fa')).add_to(mCluster)
    #             continue
    #         folium.Marker(coordinate, popup = popup, icon = folium.Icon(color = 'green', icon='bicycle', prefix='fa')).add_to(mCluster)

    #     folium.LayerControl().add_to(m)
        
    #     context = {'map': m._repr_html_(), 'gu_dong_mapping' : gu_dong_mapping}
    #     return render(request, "map.html", context)


def show_bike_list(request):

    gu_name = request.GET.get('addr2')
    dong_name = request.GET.get('addr3')

    bike_list = Station.objects.filter(gu = gu_name, dong = dong_name).values('stationName', 'parkingBikeTotCnt', 'gu', 'dong')
    return JsonResponse(list(bike_list), safe=False)



def pollenbike (request):
    return render(request, "pollenbike.html")
