from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class City(Base):
    __tablename__ = "city"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    name = Column(String(30))

    def __repr__(self):
        return f"({self.name=}, {self.id=})"


class HttpCode(Base):
    __tablename__ = "http_code"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    code = Column(String(3), unique=True)
    description = Column(String(60))

    def __repr__(self):
        return f"({self.code=}, {self.id=})"


class HttpLog(Base):
    __tablename__ = "http_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    request = Column(String, nullable=False)
    response = Column(String, nullable=False)
    code_id = Column(UUID(as_uuid=True), ForeignKey('http_code.id'))

    code = relationship('HttpCode', lazy=False, uselist=False, foreign_keys=[code_id])


class WeatherInfo(Base):
    __tablename__ = "weather_info"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    http_log_id = Column(UUID(as_uuid=True), ForeignKey('http_log.id'))
    city_id = Column(UUID(as_uuid=True), ForeignKey('city.id'))
    distance = Column(Float)
    current_temperature = Column(Float)
    relative_humidity = Column(Float)
    last_updated_datetime = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    execution_identifier = Column(String)

    city = relationship('City', lazy=False, uselist=False, foreign_keys=[city_id])

    def __repr__(self):
        return (
            f"({self.distance=}, "
            f"{self.current_temperature=}, "
            f"{self.relative_humidity=}, "
            f"{self.last_updated_datetime=}, "
            f"{self.city.name if self.city else None})"
        )

    def dict(self):
        return {
            "distance": self.distance,
            "current_temperature": self.current_temperature,
            "relative_humidity": self.relative_humidity,
            "last_updated_datetime": self.last_updated_datetime,
        }
