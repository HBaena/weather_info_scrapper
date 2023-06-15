from dataclasses import dataclass, asdict, is_dataclass
from datetime import date, datetime, time
from json import dumps, JSONEncoder
from logging import getLogger
from typing import Any, Optional


logger = getLogger()


class JSONEncoder(JSONEncoder):
    def default(self, obj):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(obj, datetime):
            result = obj.isoformat()
            if obj.microsecond:
                result = result[:23] + result[26:]
            if result.endswith('+00:00'):
                result = result[:-6] + 'Z'
            return result
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, time):
            result = obj.isoformat()
            if obj.microsecond:
                result = result[:12]
            return result
        else:
            return super().default(obj)


class BaseModel:
    def dict(self) -> dict:
        response = asdict(self)
        return {
            key: (
                value.dict() if is_dataclass(value) else value
            ) for key, value in response.items()
        }

    def json(self, indent=2) -> str:
        return dumps(self.dict(), indent=indent, cls=JSONEncoder)


@dataclass
class RequestInfo(BaseModel):
    status_code: int
    request: str
    scrapped_info: Optional[Any]
    id: str
