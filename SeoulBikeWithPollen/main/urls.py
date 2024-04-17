from django.conf import settings
from django.urls import path, include
from . import views
# from .views import *
from django.conf.urls import static

urlpatterns = [
    # path('', views.bike_station_info, name='bike_station_info'),
    path('', views.index, name='main'),
    path('<str:addr1>_<str:addr2>/', views.index_now, name='now'),
    path('home/', views.home, name='home'),
    path('kakaomap/', views.kakaomap, name='kakaomap'),
    path('header/', views.header, name='header'),
    path('sidebar/', views.sidebar, name='sidebar'),
    path('svgT2/', views.svgT2, name='svgT2'),
    path('svgT1/', views.svgT1, name='svgT1'),
]