from logging import getLogger
from database.repositories import WeatherInfoRepository
from src.adapters.document_storage.interface import DocumentStorageInterface
from src.domain.resume import get_weather_info_parquet_file

logger = getLogger()


class DBResumeSaver:
    def __init__(
        self,
        weather_info_repository: WeatherInfoRepository,
        document_storage_adapter: DocumentStorageInterface,
        parquet_file_generator,
    ):
        self.weather_info_repository = weather_info_repository
        self.document_storage_adapter = document_storage_adapter
        self.parquet_file_generator = parquet_file_generator

    def execute(self):
        try:
            parquet_file = get_weather_info_parquet_file(
                self.weather_info_repository,
                self.parquet_file_generator,
            )
            error = self.document_storage_adapter.save_file(
                filename="resumes.parquet",
                content=parquet_file,
            )
            if error:
                raise error
            return "SUCCESS"
        except Exception as error:
            print(error)
            return "ERROR"
