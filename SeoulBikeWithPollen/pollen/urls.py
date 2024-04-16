from django.urls import path
from .views import *

app_name = 'pollen'

urlpatterns = [
    path('', PollenInputView.as_view()),
    path('api/', PollenApiView.as_view(),name='addrCode'),
]