from sys import argv
import logging
from src.handler.weather_info_extractor.handler import handler
from datetime import datetime


all_cities = [
    "ciudad-de-mexico",
    "monterrey",
    "merida",
    "wakanda"
]
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    format='%(name)s - %(levelname)s - %(message)s',
)

if __name__ == '__main__':
    cities = argv[1]
    execution_datetime = datetime.now()
    logging.info(f"{execution_datetime=}")
    logging.info(f"{cities=}")
    if cities == "all":
        cities = all_cities
    else:
        cities = cities.split(",")
    for city in cities:
        logging.info(f"{city=}")
        logging.info(handler(city=city, execution_identifier=execution_datetime.timestamp()))
