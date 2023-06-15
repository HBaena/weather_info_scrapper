from os import getenv, path, getcwd


JSON_FILES_LOCATION = getenv("JSON_FILES_LOCATION", path.join(getcwd(), "json_files"))
RESUME_FILE_LOCATION = getenv("RESUME_FILE_LOCATION", path.join(getcwd(), "resumes"))
BASE_WEATHER_INFO_URL = getenv("BASE_WEATHER_INFO_URL", "https://www.meteored.mx/{city}/historico")
DB_HOSTNAME = getenv("DB_HOSTNAME")
DB_USER = getenv("DB_USER")
DB_PORT = getenv("DB_PORT")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")
