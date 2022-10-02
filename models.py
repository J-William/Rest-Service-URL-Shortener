from pydantic import BaseModel, HttpUrl
import uuid
from utilities import base62encode


class MappingRequest(BaseModel):
    original_url : HttpUrl


class Mapping():
    def __init__(self, ourl: HttpUrl):
        self.original_url = ourl
        self.uid = uuid.uuid4().int
        self.mapKey = self.generate_mapKey(self.uid)

    @staticmethod
    def generate_mapKey(num: int):
        """Truncate the uid and base62 encode to generate a short alias"""
        num = int(str(num)[:8])
        return base62encode(num)


