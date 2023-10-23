from dataclasses import dataclass
from pydantic import BaseModel, HttpUrl


class MappingRequest(BaseModel):
    """ FastAPI request model"""
    url : HttpUrl


@dataclass(frozen=True)
class Mapping:
    """ An original url and mapkey pair"""
    url : HttpUrl
    mapkey : str 





