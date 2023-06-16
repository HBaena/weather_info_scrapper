# weather_info_scrapper

The project works like a weather info scrapper with a data flow consisting of srcapp info, save request info, save scrapped info, make a db resume and backup into a parquet file
It was developed using a adapter desing patter with clean code and tdd. It is prepared to use it easely as AWS lambdas

## Dependencies
- [poetry](https://python-poetry.org/docs/)
- You should have a postgresql database prepared and add security value to .env
```.env
DB_HOSTNAME=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=12345
DB_NAME=test_dd360
```
## Init
After all install dependencies and create db tables
```bash
make init
```
## Develop
```bash
make init lint test
```
## Run scrapper
```bash
make run
```

This will install python dependencies and run airflow scheduler

![image](https://github.com/HBaena/weather_info_scrapper/assets/39740586/9847cdf1-f240-4d0b-b615-df555674ffe6)

Each hour it will scrapp weather info from certain cities, save a json, save it to db and then, make a db resume into a .parquet\

![image](https://github.com/HBaena/weather_info_scrapper/assets/39740586/b58fe1af-0a26-4619-a9cd-f92629c63477)

![image](https://github.com/HBaena/weather_info_scrapper/assets/39740586/fe7c045b-25a1-4e09-b367-018f4d6be424)

A json generated example is like:
```json
{
  "status_code": 200,
  "request": "-----------START-----------\nGET https://www.meteored.mx/monterrey/historico\r\nUser-Agent: python-requests/2.31.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\nNone",
  "scrapped_info": {
    "distance": 23.9,
    "current_temperature": 32.0,
    "relative_humidity": 40.8,
    "last_updated_datetime": "2023-06-15T04:40:00"
  },
  "id": "2023-06-14T23:30:09.933193monterrey"
}
```
A example of a db resume is like:
```
               name execution_identifier  max_temperature  min_temperature  avg_temperature  max_rh  min_rh  avg_rh        last_updated
0         monterrey    1686895244.645699             31.0             31.0             31.0    62.5    62.5    62.5 2023-06-16 04:40:00
1  ciudad de mexico    1686810491.513326             24.0             24.0             24.0    41.2    41.2    41.2 2023-06-15 04:45:00
2         monterrey    1686896965.779344             31.0             31.0             31.0    62.5    62.5    62.5 2023-06-16 04:40:00
3         monterrey     1686811036.55464             33.0             33.0             33.0    38.5    38.5    38.5 2023-06-15 05:40:00
4         monterrey    1686896972.858381             31.0             31.0             31.0    62.5    62.5    62.5 2023-06-16 04:40:00
```

## Dashboard
```bash
make install run_dashboard
```
Once server is running, enter into http://127.0.0.1:8050/
### Dashboard made using Dash by Plotly
![image](https://github.com/HBaena/weather_info_scrapper/assets/39740586/6e7c5f0b-053b-4cfc-ba97-97d87bd3d161)
![image](https://github.com/HBaena/weather_info_scrapper/assets/39740586/35599cee-1293-41e5-9e9d-8f849e025da3)
### You can filter by `city` and order by any column
![image](https://github.com/HBaena/weather_info_scrapper/assets/39740586/fd19258e-03d8-4603-858b-669e019f0a75)
 

## Possible improvements
- Tests
    - As I developed this project in a short time, I don't wanted to spent a lot of time patching some modelues in some utils, adapters or handlers. So, an important improvement is to make a better dependencies injections to be able to test easly each compenent without the need of patching modules 
- Adapters
    - I prepare the adapters interface to easily integrate another document storage like S3, ftp or so on. Also another scrapper client like scrapy could be added without the need of modify the app logic.
- Dashboard
    - The web page style could be improved
- Dockerize
- Change the workflow
    - Currently the project only have 2 airflow tasks: scrapping and save db resume. Scrapping task could be separated into: scrapp and save request json, retrieve info from http response and save into db in individual tasks
- Add db migrations tool like [Alembic](https://alembic.sqlalchemy.org/en/latest/)
