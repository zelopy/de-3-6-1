from django.db import models

# Create your models here.
class SeoulBikeStationInfo(models.Model):
    # 대여소 ID
    station_id = models.IntegerField(verbose_name="대여소 ID")
    # 대여소 이름
    station_name = models.CharField(max_length=100, verbose_name="대여소 이름")
    # 거치대 수
    raccnt = models.ImageField(verbose_name="거치대 수")
    # 대여소 구
    addr1 = models.CharField(max_length=20, verbose_name="구")
    # 대여소 동
    addr2 = models.CharField(max_length=20, verbose_name="동")
    # 대여소 위도
    latitude = models.FloatField()
    # 대여소 경도
    longitude = models.FloatField()

class SeoulBikeStationNow(models.Model):
    station = models.ForeignKey(SeoulBikeStationInfo, related_name='now', on_delete=models.CASCADE)
    # 자전거 거치 수
    bikecnt = models.IntegerField(verbose_name="자전거 수")
    # 자전거 거치율
    bikeratio = models.IntegerField(verbose_name="거치율")