from django.urls import path
from map import views

app_name ='map'
urlpatterns = [
    path('', views.map, name='map'),
    path('list', views.show_bike_list, name='list'),
    path('temp/', views.pollenbike, name='temp')
]
