from logging import getLogger
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database.models import City, WeatherInfo, HttpLog, HttpCode


logger = getLogger()


class BaseRepository:
    def __init__(self, engine, model):
        self.__engine = engine
        self.__model = model

    def save(self, instance):
        with Session(self.__engine, expire_on_commit=False) as session:
            try:
                session.add(instance)
                session.commit()
                return instance
            except Exception as error:
                logger.erro(error)
                session.rollback()

    def create(self, **kwargs):
        instance = self.__model(**kwargs)
        return self.save(instance)

    def get_all(self):
        with Session(self.__engine) as session:
            return session.query(self.__model).all()

    def get_by_name(self, name):
        with Session(self.__engine) as session:
            return session.query(self.__model).where(self.__model.name == name).first()

    def get_by_id(self, id):
        with Session(self.__engine) as session:
            return session.query(self.__model).where(self.__model.id == id).first()


class WeatherInfoRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine, WeatherInfo)
        self.__engine = engine
        self.__model = WeatherInfo

    def get_resume(self):
        with Session(self.__engine) as session:
            return session.query(
                City.name,
                WeatherInfo.execution_identifier,
                func.max(WeatherInfo.current_temperature).label('max_temperature'),
                func.min(WeatherInfo.current_temperature).label('min_temperature'),
                func.avg(WeatherInfo.current_temperature).label('avg_temperature'),
                func.max(WeatherInfo.relative_humidity).label('max_rh'),
                func.min(WeatherInfo.relative_humidity).label('min_rh'),
                func.avg(WeatherInfo.relative_humidity).label('avg_rh'),
                func.max(WeatherInfo.last_updated_datetime).label('last_updated')
            ).join(
                City, WeatherInfo.city_id == City.id,
            ).group_by(
                City.name,
                WeatherInfo.execution_identifier,
            )


class CityRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine, City)
        self.__engine = engine
        self.__model = WeatherInfo


class HttpCodeRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine, HttpCode)
        self.__engine = engine
        self.__model = HttpCode

    def get_by_code(self, code):
        with Session(self.__engine) as session:
            return session.query(self.__model).where(self.__model.code == code).first()


class HttpLogRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine, HttpLog)
        self.__engine = engine
        self.__model = HttpLog

    def create(self, status_code, *args, **kwargs):
        code_repository = HttpCodeRepository(engine=self.__engine)
        code = code_repository.get_by_code(code=str(status_code))
        return super().create(code_id=code.id, *args, **kwargs)
