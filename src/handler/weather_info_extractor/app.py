from datetime import datetime
from logging import getLogger
from typing import Type

from database.models import HttpLog, WeatherInfo
from database.repositories import CityRepository, HttpLogRepository, WeatherInfoRepository
from src.adapters.scrapper.interface import ScrapperInterface
from src.adapters.document_storage.interface import DocumentStorageInterface
from src.domain.scrapping import get_weather_info
from src.utils.request import format_request
from src.utils.models import RequestInfo


logger = getLogger()


class WeatherInfoExtractor:
    def __init__(
        self,
        scrapper_adapter_class: Type[ScrapperInterface],
        document_storage_adapter: DocumentStorageInterface,
        weather_info_repository: WeatherInfoRepository,
        city_repository: CityRepository,
        http_log_repository: HttpLogRepository,
        base_url: str,
        city: str,
        execution_identifier: str,
    ):
        self.weather_info_repository = weather_info_repository
        self.city_repository = city_repository
        self.http_log_repository = http_log_repository
        self.scrapper_adapter_class = scrapper_adapter_class
        self.document_storage_adapter = document_storage_adapter
        self.city = city
        self.execution_identifier = str(execution_identifier)
        self.full_url = base_url.format(city=city)
        self.scrapper_adapter = self.scrapper_adapter_class(
            url=self.full_url
        )

    def execute(self):
        html_body = self.scrapper_adapter.get_html()
        weather_info = get_weather_info(self.scrapper_adapter) if html_body else None
        print(weather_info)
        request_info = self.__save_json_file(weather_info)
        http_log = self.__save_http_response(request_info)
        if not weather_info:
            return
        self.__save_to_database(weather_info, http_log)
        return weather_info.dict()

    def __save_json_file(self, weather_info: WeatherInfo):
        request_info = RequestInfo(
            status_code=self.scrapper_adapter.http_response.status_code,
            request=format_request(self.scrapper_adapter.http_request),
            scrapped_info=weather_info.dict() if weather_info else None,
            id=f"{datetime.now().isoformat()}-{self.city}",
        )
        error = self.document_storage_adapter.save_file(
            filename=f"{request_info.id}.json",
            content=request_info.json(),
        )
        if error:
            # do something
            logger.error(error)
        return request_info

    def __save_http_response(self, request_info: RequestInfo) -> HttpLog:
        return self.http_log_repository.create(
            request=request_info.request,
            response=self.scrapper_adapter.http_response.text,
            status_code=request_info.status_code,
        )

    def __save_to_database(self, weather_info: WeatherInfo, http_log: HttpLog):
        city = self.city_repository.get_by_name(self.city.replace("-", " "))
        weather_info.city_id = city.id
        weather_info.http_log_id = http_log.id
        weather_info.execution_identifier = self.execution_identifier
        instance = self.weather_info_repository.save(weather_info)
        if not instance:
            # do something
            ...
