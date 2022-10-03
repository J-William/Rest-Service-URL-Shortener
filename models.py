from dataclasses import dataclass
from pydantic import BaseModel, HttpUrl
from utilities import generate_mapKey


class MappingRequest(BaseModel):
    original_url : HttpUrl


class Mapping():
    def __init__(self, ourl: HttpUrl):
        self.original_url = ourl
        self.mapKey = generate_mapKey()



