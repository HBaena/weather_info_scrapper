from unittest.mock import call, Mock

from expects import expect, equal, be_true
from faker import Faker
from freezegun import freeze_time
from mamba import after, before, context, describe, it

from src.utils.request import format_request
from src.utils.models import RequestInfo
from src.handler.weather_info_extractor.app import WeatherInfoExtractor

fake = Faker()

with describe(WeatherInfoExtractor) as self:
    with before.all:
        self.now = fake.date_time()
        self.freezer = freeze_time(self.now)
        self.freezer.start()
        self.base_url = "SOME_BASE_URL_TEMPLATED/{city}"
        self.city = "SOME-CITY"
        self.full_url = "SOME_BASE_URL_TEMPLATED/SOME-CITY"
        self.execution_identifier = "SOME_EXECUTION_IDENTIFIER"
        self.html_body = "SOME_HTML"
        self.distance = fake.pyfloat()
        self.current_temperature = fake.pyfloat()
        self.relative_humidity = fake.pyfloat()
        self.last_updated_datetime = fake.date_time()
        self.http_request = Mock(
            method="GET",
            url=self.full_url,
            body="SOME_BODY",
            headers={},
        )

    with before.each:
        self.scrapper_adapter = Mock()
        self.scrapper_adapter.get_html.return_value = self.html_body
        self.scrapper_adapter_class = Mock()
        self.document_storage_adapter = Mock()
        self.weather_info_repository = Mock()
        self.city_repository = Mock()
        self.http_log_repository = Mock()
        self.scrapper_adapter_class.return_value = self.scrapper_adapter
        self.scrapper_adapter.get_text_by_span_id.side_effect = [
            f"{self.distance}km",
            str(self.relative_humidity),
            str(self.current_temperature),
            self.last_updated_datetime.strftime("%d/%m/%Y %H:%M:%S"),
        ]
        self.json_content = RequestInfo(
            status_code=200,
            request=format_request(self.http_request),
            scrapped_info={
                "distance": self.distance,
                "current_temperature": self.current_temperature,
                "relative_humidity": self.relative_humidity,
                "last_updated_datetime": self.last_updated_datetime,
            },
            id=f"{self.now.isoformat()}-{self.city}",
        )

    with after.all:
        self.freezer.stop()

    with context("when all works"):
        with it("should return weather info"):
            self.scrapper_adapter.http_response.status_code = 200
            self.scrapper_adapter.http_response.text = "SOME_TEXT"
            self.scrapper_adapter.http_request = self.http_request
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

            expect(self.scrapper_adapter_class.call_args).to(equal(call(url=self.full_url)))
            expect(len(self.scrapper_adapter.get_text_by_span_id.call_args_list)).to(equal(4))
            expect(self.scrapper_adapter.get_text_by_span_id.call_args_list[0]).to(equal(call("dist_cant")))
            expect(self.scrapper_adapter.get_text_by_span_id.call_args_list[1]).to(equal(call("ult_dato_hum")))
            expect(self.scrapper_adapter.get_text_by_span_id.call_args_list[2]).to(equal(call("ult_dato_temp")))
            expect(self.scrapper_adapter.get_text_by_span_id.call_args_list[3]).to(equal(call("fecha_act_dato")))
            expect(self.scrapper_adapter.get_html.called).to(be_true)
            expect(self.document_storage_adapter.save_file.call_args).to(equal(call(
                filename=f"{self.now.isoformat()}-{self.city}.json",
                content=self.json_content.json(),
            )))
            expect(self.http_log_repository.create.call_args).to(equal(call(
                request=self.json_content.request,
                status_code=200,
                response="SOME_TEXT",
            )))
            expect(self.city_repository.get_by_name.call_args).to(equal(call("SOME CITY")))
            expect(response).to(equal({
                'distance': self.distance,
                'current_temperature': self.current_temperature,
                'relative_humidity': self.relative_humidity,
                'last_updated_datetime': self.last_updated_datetime,
            }))
