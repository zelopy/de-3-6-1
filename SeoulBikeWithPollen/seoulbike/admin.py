from django.contrib import admin
from .models import *

# Register your models here.
class StationAdmin(admin.ModelAdmin):  #admin 계정에서 보기 이쁘게 만들어주는 함수
    fieldsets = [
        ('대여소', {'fields': ['station_name']}),
        ('주소', {'fields': ['addr1', 'addr2']}),  #숨기고 싶을 때 classes에 collapse를 준다
    ]
    list_display = ('station_name', 'addr1', 'addr2')
    search_fields=['station_name', 'addr1', 'addr2']     #검색 기능

admin.site.register(SeoulBikeStationInfo, StationAdmin)