from django.urls import path
from .views import *

app_name = 'pollen'

urlpatterns = [
    path('', PollenApiView.as_view()),
]