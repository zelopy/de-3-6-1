import pandas as pd
from .models import SeoulBikeStationInfo
import os

def import_csv_to_model(csv_file_path):
    df = pd.read_csv(csv_file_path, sep=',')
    df = df.rename(columns={"station_lat":"latitude", "station_lon":"longitude", "ADM_NM":"addr2","gu":"addr1"}).drop(df.columns[0], axis=1)
    for row in df.itertuples():
        station_id = row.station_id
        station_name = row.station_name
        raccnt = int(row.raccnt)
        addr1 = row.addr1
        addr2 = row.addr2
        latitude = float(row.latitude)
        longitude = float(row.longitude)

        station_info = SeoulBikeStationInfo.objects.create(
            station_id=station_id,
            station_name=station_name,
            raccnt=raccnt,
            addr1=addr1,
            addr2=addr2,
            latitude=latitude,
            longitude=longitude
        )

    print("CSV 파일을 모델에 성공적으로 입력했습니다.")

if __name__ == '__main__':
    print(os.listdir())
    import_csv_to_model('../seoulblikeinfo.csv')