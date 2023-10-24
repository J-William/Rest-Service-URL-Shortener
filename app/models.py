from pydantic import BaseModel, HttpUrl
from typing import Self
from app.utilities import generate_shortcut
from app.persistence import (
    save_db_mapping, save_cache_mapping, search_cache_by_url,
    search_cache_by_shortcut, search_db_by_shortcut, search_db_by_url
)


class MappingRequest(BaseModel):
    """ FastAPI request model"""
    url: HttpUrl


class Mapping:
    """ An original url and shortcut pairing."""

    def __init__(self, url: str, shortcut: str = None):
        self.url = url
        self.shortcut = shortcut if shortcut else generate_shortcut()

    @classmethod
    def find(cls, url: str = None, shortcut: str = None) -> Self | None:
        """ Search the persistence layer for a Mapping."""
        res = None
        if url:
            res = search_cache_by_url(url)
            if not res:
                res = search_db_by_url(url)

        if shortcut:
            res = search_cache_by_shortcut(shortcut)
            if not res:
                res = search_db_by_shortcut(shortcut)

        if res:
            return Mapping(url=res['url'], shortcut=res['_id'])
        else:
            return None

    def save(self):
        """ Persist a Mapping to the cache and db."""
        save_db_mapping(url=self.url, shortcut=self.shortcut)
        save_cache_mapping(url=self.url, shortcut=self.shortcut)
