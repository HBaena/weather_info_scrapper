import fastparquet
from io import BytesIO
import pandas as pd
from database.repositories import WeatherInfoRepository


def get_weather_info_parquet_file(
        weather_info_repository: WeatherInfoRepository,
        parquet_file_generator=fastparquet
):
    query = weather_info_repository.get_resume()
    df = pd.read_sql(query.statement, query.session.bind)
    bytes_io = BytesIO()
    bytes_io.close = lambda: None
    fastparquet.write(bytes_io, df, partition_on="execution_identifier")

    return bytes_io.getvalue()
