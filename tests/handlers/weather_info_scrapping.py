from unittest.mock import call, Mock
from mamba import before, context, describe, it

from expects import be_false, be_none, expect, equal, be_true
from faker import Faker
from src.handler.weather_info_extractor.app import WeatherInfoExtractor

fake = Faker()

with describe(WeatherInfoExtractor) as self:
    with before.all:
        self.base_url = "SOME_BASE_URL"
        self.city = "SOME_CITY"
        self.execution_identifier = "SOME_EXECUTION_IDENTIFIER"
        self.distance = fake.pyfloat()
        self.current_temperature = fake.pyfloat()
        self.relative_humidity = fake.pyfloat()
        last_updated_datetime = fake.date_time()

    with before.each:
        self.scrapper_adapter_class = Mock()
        self.document_storage_adapter = Mock()
        self.weather_info_repository = Mock()
        self.city_repository = Mock()
        self.http_log_repository = Mock()

    with context("when all works"):
        with fit("should return weather info"):
            executor = WeatherInfoExtractor(
                scrapper_adapter_class=self.scrapper_adapter_class,
                document_storage_adapter=self.document_storage_adapter,
                weather_info_repository=self.weather_info_repository,
                city_repository=self.city_repository,
                http_log_repository=self.http_log_repository,
                base_url=self.base_url,
                city=self.city,
                execution_identifier=self.execution_identifier,
            )

            response = executor.execute()

            expect(response).to(equal({
                'distance': self.distance,
                'current_temperature': self.current_temperature,
                'relative_humidity': self.relative_humidity,
                'last_updated_datetime': self.last_updated_datetime,
            }))
