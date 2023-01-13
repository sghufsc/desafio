from datetime import datetime
from marshmallow import Schema, fields
from pytz import timezone

class BaseModel(Schema):
    pass

class LocalTime(fields.Field):
    def get_local_time(self):
        return datetime.now(tz=timezone('America/Sao_Paulo'))

    def __new__(cls):
       return fields.Field(load_default=cls.get_local_time(cls), dump_default=cls.get_local_time(cls))