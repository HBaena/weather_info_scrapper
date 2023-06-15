import fastparquet
from database.repositories import WeatherInfoRepository
from database.utils import get_engine
from src.handler.save_db_resume.app import DBResumeSaver
from src.config import RESUME_FILE_LOCATION
from src.adapters.document_storage.factory import get_adapter

engine = get_engine()


def handler(*args, **kwargs):
    return DBResumeSaver(
        weather_info_repository=WeatherInfoRepository(engine),
        document_storage_adapter=get_adapter("local")(root_location=RESUME_FILE_LOCATION),
        parquet_file_generator=fastparquet,
    ).execute()
