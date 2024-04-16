from django.urls import path
from .views import *

app_name = 'pollen'

urlpatterns = [
    path('', PollenApiView.as_view()),
    # TODO : 행정구역코드 목록
    path('addr_list/', PollenAddrListView.as_view()),
]