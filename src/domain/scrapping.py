from datetime import datetime
from logging import getLogger

from src.adapters.scrapper.interface import ScrapperInterface
from database.models import WeatherInfo

logger = getLogger()


def get_weather_info(soup: ScrapperInterface) -> WeatherInfo:
    distance = soup.get_text_by_span_id("dist_cant")
    relative_humidity = soup.get_text_by_span_id("ult_dato_hum")
    current_temperature = soup.get_text_by_span_id("ult_dato_temp")
    updated_at = soup.get_text_by_span_id("fecha_act_dato")
    if distance := distance:
        try:
            distance = float(distance[:-2])
        except Exception as error:
            logger.info("distance")
            logger.info(error)

    if current_temperature := current_temperature:
        try:
            current_temperature = float(current_temperature)
        except Exception as error:
            logger.info("current_temperature")
            logger.info(error)

    if relative_humidity := relative_humidity:
        try:
            relative_humidity = float(relative_humidity)
        except Exception as error:
            logger.info("relative_humidity")
            logger.info(error)

    if updated_at := updated_at:
        try:
            updated_at = datetime.strptime(updated_at, "%d/%m/%Y %H:%M:%S")
        except Exception as error:
            logger.info("updated_at")
            logger.info(error)

    return WeatherInfo(
        distance=distance,
        current_temperature=current_temperature,
        last_updated_datetime=updated_at,
        relative_humidity=relative_humidity,
    )
