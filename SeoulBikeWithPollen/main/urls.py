from django.conf import settings
from django.urls import path, include
from . import views
# from .views import *
from django.conf.urls import static

urlpatterns = [
    path('', views.index, name='main'),
    path('home/', views.home, name='home'),
    path('kakaomap/', views.kakaomap, name='kakaomap'),
]