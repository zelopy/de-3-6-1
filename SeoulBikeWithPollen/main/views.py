from django.shortcuts import render
import folium
from .latlon_to_dong import ress


def index(request):
    # 데이터를 가져와서 Folium 지도에 표시
    m = folium.Map(location=[37.56, 127], zoom_start=8)
    for index, row in ress.iterrows():
        
        radius = row['rackTotCnt'] / 2
        circle_marker = folium.CircleMarker(location=[row['stationLatitude'], row['stationLongitude']],
                                            radius=radius,
                                            color='blue',
                                            fill=True,
                                            fill_color='blue',
                                            fill_opacity=0.6)

        
        popup = folium.Popup(f'<p><strong>{row["rackTotCnt"]}</strong></p><p>{row["stationName"]}</p>', max_width=500)
        circle_marker.add_child(popup)

        
        circle_marker.add_to(m)

    map_html = m._repr_html_()

    context = {
        'map_html': map_html,
    }
    return render(request, 'index.html', context)
