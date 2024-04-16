from django.db import models

# Create your models here.
class Station(models.Model):
    rackTotCnt = models.IntegerField()  
    stationName = models.CharField(max_length=30)
    parkingBikeTotCnt = models.IntegerField()
    shared = models.IntegerField()
    stationLatitude = models.FloatField()
    stationLongitude = models.FloatField()
    stationId = models.CharField(max_length=30)
    # gu = models.CharField(max_length=30)
    # dong = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.stationName}, 대여 가능 자전거 수 = {self.parkingBikeTotCnt}"