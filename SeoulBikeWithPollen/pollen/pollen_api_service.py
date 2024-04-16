import requests
import json
from datetime import datetime
import os
import sqlite3

# 기상청_꽃가루농도위험지수 조회서비스(3.0)
'''
* 꽃가루농도위험지수 단계 및 범위
    낮음 : 0
    보통 : 1
    높음 : 2
    매우높음 : 3

* 데이터 생산 시간
    06시 (오늘,내일,모레)
    18시 (내일,모레,글피)

* 데이터 제공 기간
    참나무 : 4월~6월
    소나무 : 4월~6월
    잡초류 : 8월~10월

* 에러 코드
    00	NORMAL_SERVICE	정상
    01	APPLICATION_ERROR	어플리케이션 에러
    02	DB_ERROR	데이터베이스 에러
    03	NODATA_ERROR	데이터없음 에러
    04	HTTP_ERROR	HTTP 에러
    05	SERVICETIME_OUT	서비스 연결실패 에러
    10	INVALID_REQUEST_PARAMETER_ERROR	잘못된 요청 파라메터 에러
    11	NO_MANDATORY_REQUEST_PARAMETERS_ERROR	필수요청 파라메터가 없음
    12	NO_OPENAPI_SERVICE_ERROR	해당 오픈API서비스가 없거나 폐기됨
    20	SERVICE_ACCESS_DENIED_ERROR	서비스 접근거부
    21	TEMPORARILY_DISABLE_THE_SERVICEKEY_ERROR	일시적으로 사용할 수 없는 서비스 키
    22	LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR	서비스 요청제한횟수 초과에러
    30	SERVICE_KEY_IS_NOT_REGISTERED_ERROR	등록되지 않은 서비스키
    31	DEADLINE_HAS_EXPIRED_ERROR	기한만료된 서비스키
    32	UNREGISTERED_IP_ERROR	등록되지 않은 IP
    33	UNSIGNED_CALL_ERROR	서명되지 않은 호출
    99	UNKNOWN_ERROR	기타에러
'''

'''
꽃가루 농도 조회
    
    Parameters : 
        pollen_type : 꽃가루 종류
            pine : 소나무
            weeds : 잡초류
            oak : 참나무
        area_no : 행정구역코드
    Returns : 
        JSON
'''
def get_pollen_data(pollen_type, area_no):
    # 공공데이터포털에서 발급받은 인증키
    key_file = './SeoulBikeWithPollen/pollen/pollen_key.json'
    with open(key_file) as f:
        key_json = json.load(f)
    service_key = key_json.get('SERVICE_KEY', '')
    # 한 페이지 결과 수 Default: 10
    num_of_rows = 10
    # 페이지 번호 Default: 1
    page_no = 1
    # 요청자료형식(XML/JSON) Default: XML
    data_type = "JSON"
    # area_no_list.xlsx 파일 참고 (ex> 서울특별시 : 1100000000)
    # area_no = 1100000000
    if area_no is None:
        return "행정구역코드가 없습니다."
    # 2024041018 (형식 : yyyyMMddHH, 최근 1일 간의 자료만 제공)
    time = datetime.now().strftime('%Y%m%d%H')

    # 꽃가루 농도 위험 지수(소나무) 조회
    if pollen_type == 'pine':
        type_str = 'getPinePollenRiskIdxV3'
    # 꽃가루 농도 위험 지수(잡초류) 조회
    elif pollen_type == 'weeds':
        type_str = 'getWeedsPollenRiskIdxV3'
    # 꽃가루 농도 위험 지수(참나무) 조회
    elif pollen_type == 'oak':
        type_str = 'getOakPollenRiskIdxV3'

    url = f"https://apis.data.go.kr/1360000/HealthWthrIdxServiceV3/{type_str}?serviceKey={service_key}&numOfRows={num_of_rows}&pageNo={page_no}&dataType={data_type}&areaNo={area_no}&time={time}"
    
    response = requests.get(url)
    contents = response.text

    '''
    * 응답 값
        code : 지수코드
        areaNo : 지점코드
        date : 발표시간
        today : 오늘 예측값 (0~3)
        tomorrow : 내일 예측값 (0~3)
        dayaftertomorrow : 모레 예측값 (0~3)
        todaysaftertomorrow : 글피 예측값 (0~3)
    '''
    json_obj = json.loads(contents)
    print(json_obj)

    return json_obj

# TEST
# print(os.getcwd())
# get_pollen_data('pine', 1100000000)


'''
구, 동, 행정구역코드 목록 조회 함수.
db.sqlite3 오류로 pollen_db.sqlite3 파일 별도로 생성하여 사용함.
    
    Parameters : addr2 (행정구 Ex> 중구, 강남구, 구로구, etc)
    
    Returns : Dict (요청 포맷은 아래 참고)
        dummy_data = [
            {'addr2': '성동구', 'addr3': [
                {'name': '행당제1동', 'addr_code': '1120056000'},
                {'name': '행당제2동', 'addr_code': '1120056001'},
                {'name': '응봉동', 'addr_code': '1120056002'},
                {'name': '금호1가동', 'addr_code': '1120056003'},
                {'name': '금호2.3가동', 'addr_code': '1120056004'}
            ]},
            {'addr2': '광진구', 'addr3': [
                {'name': '군자동', 'addr_code': '1121573000'},
                {'name': '중곡제1동', 'addr_code': '1121574000'},
                {'name': '중곡제2동', 'addr_code': '1121575000'},
                {'name': '중곡제3동', 'addr_code': '1121576000'},
                {'name': '중곡제4동', 'addr_code': '1121577000'}
            ]},
            {'addr2': '송파구', 'addr3': [
                {'name': '거여1동', 'addr_code': '1171053100'},
                {'name': '거여2동', 'addr_code': '1171053200'},
                {'name': '마천1동', 'addr_code': '1171054000'},
                {'name': '마천2동', 'addr_code': '1171055000'},
                {'name': '방이1동', 'addr_code': '1171056100'}
            ]}
        ]
'''
def addr_code_list(addr2):
    # print(f'addr_code_list({addr2})')
    db_file = './pollen/pollen_db.sqlite3'
    check = os.path.isfile(db_file)
    # print(f'os.getcwd(): {os.getcwd()}')
    # print(f'check: {check}')

    # conn = sqlite3.connect('./SeoulBikeWithPollen/pollen/pollen_db.sqlite3')
    conn = sqlite3.connect('./pollen/pollen_db.sqlite3')
    cursor = conn.cursor()
    
    if addr2 != '':
        # addr2에 포함되는 목록
        cursor.execute("SELECT * FROM seoul_area_no_list WHERE addr2 = ? AND addr3 IS NOT NULL", [addr2])
    else:
        # 전체 목록
        cursor.execute("SELECT * FROM seoul_area_no_list WHERE addr3 IS NOT NULL")

    result = []
    addr2_tmp = None
    addr3_list = []

    rowList = cursor.fetchall()

    # print(f'rowList:{rowList}')

    for row in rowList:
        addr2, addr3, addr_code = row[2], row[3], str(row[0])

        if addr2_tmp != addr2:
            if addr2_tmp is not None:
                result.append({'addr2': addr2_tmp, 'addr3': addr3_list})
                addr3_list = []
            addr2_tmp = addr2
        
        addr3_list.append({'name': addr3, 'addr_code': addr_code})

    # 마지막 그룹 추가
    if addr2_tmp is not None:
        result.append({'addr2': addr2_tmp, 'addr3': addr3_list})
    
    return result


# rs = addr_code_list('강남구')
# rs = addr_code_list('')

# file_path = 'result.txt'
# with open(file_path, 'w') as file:
#     file.writelines(str(rs))

# print(rs)
