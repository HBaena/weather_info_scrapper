from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models import Base, City, HttpCode
from src.config import DB_HOSTNAME, DB_USER, DB_PORT, DB_PASSWORD, DB_NAME


def get_db_uri():
    uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
    return uri


def get_engine(*args, **kwargs):
    return create_engine(get_db_uri(), *args, **kwargs)


def populate_database(engine):
    cities = {
        "ciudad de mexico",
        "monterrey",
        "merida",
        "wakanda",
    }
    http_codes = {
        "200": "success",
        "404": "not found",
        "500": "internal server error",
    }
    with Session(engine) as session:
        session.add_all(City(name=city) for city in cities)
        session.add_all(
            HttpCode(
                code=code,
                description=description
            ) for code, description in http_codes.items()
        )
        session.commit()


def create_all():
    engine = get_engine()
    Base.metadata.create_all(engine)
    populate_database(engine)
