from django.urls import path
from . import views
from .views import *

app_name = 'pollen'

urlpatterns = [
    path('', PollenApiView.as_view()),
    # 행정구역코드 목록
    path('addr_list/', views.result, name='result'),
    path('addr_list/<str:addr2>/', views.result, name='result'),
]