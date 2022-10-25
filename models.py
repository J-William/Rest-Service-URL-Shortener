from dataclasses import dataclass
from functools import cached_property
from pydantic import BaseModel, HttpUrl
from utilities import generate_mapkey


class MappingRequest(BaseModel):
    original_url : HttpUrl


@dataclass(frozen=True)
class Mapping:
    url: HttpUrl
    
    @cached_property
    def mapkey(self) -> str:
        return generate_mapkey()




