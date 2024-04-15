from django.shortcuts import render
import folium
from .latlon_to_dong import ress


def index(request):
    # 데이터를 가져와서 Folium 지도에 표시
    m = folium.Map(location=[37.56, 127], zoom_start=8)  # Folium 지도 생성
    for index, row in ress.iterrows():
        # CircleMarker의 반지름 설정 (rackTotCnt에 따라 비례하도록 설정)
        radius = row['rackTotCnt'] / 2  # 반지름을 조절하기 위해 적절한 스케일을 선택합니다.
        circle_marker = folium.CircleMarker(location=[row['stationLatitude'], row['stationLongitude']],
                                            radius=radius,
                                            color='blue',
                                            fill=True,
                                            fill_color='blue',
                                            fill_opacity=0.6)

        # CircleMarker에 Popup 추가
        popup = folium.Popup(f'<p><strong>{row["rackTotCnt"]}</strong></p><p>{row["stationName"]}</p>', max_width=500)
        circle_marker.add_child(popup)

        # Folium 지도에 CircleMarker 추가
        circle_marker.add_to(m)

    map_html = m._repr_html_()
    # 템플릿에 전달할 context 설정
    context = {
        'map_html': map_html,
    }
    return render(request, 'index.html', context)