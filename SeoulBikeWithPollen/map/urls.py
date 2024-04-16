from django.urls import path
from map import views

app_name ='map'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_location, name='search_location'),
]
