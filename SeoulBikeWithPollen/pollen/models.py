from django.db import models

'''
addr_code : 행정구역코드
addr1 : 행정주소1(시)
addr2 : 행정주소2(구)
addr3 : 행정주소3(동)
longitude : 경도
latitude : 위도
'''
class PollenAddrCode(models.Model):
    # 행정구역코드
    addr_code = models.CharField(max_length=10, verbose_name='행정구역코드')
    # 행정주소1(시)
    addr1 = models.CharField(max_length=20, verbose_name='행정주소1(시)', default='서울특별시')
    # 행정주소2(구)
    addr2 = models.CharField(max_length=20, verbose_name='행정주소2(구)')
    # 행정주소3(동)
    addr3 = models.CharField(max_length=20, verbose_name='행정주소3(동)')
    # 경도
    longitude = models.FloatField()
    # 위도
    latitude = models.FloatField()


class PollenApi(models.Model):
    # 지수코드
    code = models.CharField(max_length=10, verbose_name='행정구역코드'),
    # 지점코드
    areaNo = models.CharField(max_length=10),
    # 발표시간
    date = models.DateField(),
    # 오늘 예측값 (0~3)
    today = models.IntegerField(),
    # 내일 예측값 (0~3)
    tomorrow = models.IntegerField(),
    # 모레 예측값 (0~3)
    dayaftertomorrow = models.IntegerField(),
    # 글피 예측값 (0~3)
    twodaysaftertomorrow = models.IntegerField()
'''
{
	'response': {
		'header': {
			'resultCode': '00', 
			'resultMsg': 'NORMAL_SERVICE'
		}, 
		'body': {
			'dataType': 'JSON', 
			'items': {
				'item': [
					{
						'code': 'D07', 
						'areaNo': '1100000000', 
						'date': '2024041518', 
						'today': '', 
						'tomorrow': '0', 
						'dayaftertomorrow': '0', 
						'twodaysaftertomorrow': '0'
					}
				]
			}, 
			'pageNo': 1, 
			'numOfRows': 10, 
			'totalCount': 1
		}
	}
}'''