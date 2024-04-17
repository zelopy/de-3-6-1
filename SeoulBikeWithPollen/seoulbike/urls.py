from django.urls import path
from .  import views
from .views import *


app_name = 'seoulbike'
urlpatterns = [
    path('', views.bike_station_info, name='bike_station_info'),
    path('<str:addr1>_<str:addr2>/', views.bike_station_now, name='now'),
]
