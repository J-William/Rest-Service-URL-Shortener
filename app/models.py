from dataclasses import dataclass
from pydantic import BaseModel, HttpUrl
from app.utilities import generate_shortcut

class MappingRequest(BaseModel):
    """ FastAPI request model"""
    url: HttpUrl


class Mapping:
    """ An original url and shortcut pairing."""

    def __init__(self, url: HttpUrl, shortcut: str):
        self.url = url
        self.shortcut = shortcut if shortcut else generate_shortcut()

    @staticmethod
    def find(self, url: HttpUrl = None, shortcut: str = None):
        """ Search the persistence layer for a Mapping."""
        pass

    def save(self):
        """ Persist a Mapping to the cache and db."""
        pass
