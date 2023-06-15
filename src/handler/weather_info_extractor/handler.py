from database.repositories import CityRepository, WeatherInfoRepository, HttpLogRepository
from database.utils import get_engine
from src.adapters.scrapper.factory import get_adapter as get_scrapper_adapter
from src.adapters.document_storage.factory import get_adapter as get_document_storage_adapter
from src.config import BASE_WEATHER_INFO_URL, JSON_FILES_LOCATION
from src.handler.weather_info_extractor.app import WeatherInfoExtractor

engine = get_engine()


def handler(*args, **kwargs):
    return WeatherInfoExtractor(
        scrapper_adapter_class=get_scrapper_adapter("BS4"),
        document_storage_adapter=get_document_storage_adapter("local")(root_location=JSON_FILES_LOCATION),
        base_url=BASE_WEATHER_INFO_URL,
        city=kwargs.get("city"),
        execution_identifier=kwargs.get("execution_identifier"),
        weather_info_repository=WeatherInfoRepository(engine),
        city_repository=CityRepository(engine),
        http_log_repository=HttpLogRepository(engine),
    ).execute()
