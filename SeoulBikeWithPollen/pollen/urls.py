from django.urls import path
from . import views
from .views import *

app_name = 'pollen'

urlpatterns = [
    path('',views.index),
    path('api/', views.PollenApiView.as_view(), name='api'),
]