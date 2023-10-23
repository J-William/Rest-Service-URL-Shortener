from typing import Any
from pydantic import HttpUrl
from app.database import DatabaseConnectionManager
from app.models import Mapping
from datetime import datetime


class MappingPersistenceManager():
    """ Database access object for managing persistence of mappings"""
    
    def __init__(self, dbcm: DatabaseConnectionManager):
        self.dbcm = dbcm
        self.connection = self.dbcm.acquire()


    def teardown(self):
        self.dbcm.release(self.connection)


    def search_url(self, url: HttpUrl) -> Mapping|None:
        """ Search for a url and retrieve the mapping if exists"""
        cursor = self.connection.driver.cursor()
        cursor.execute(""" 
                SELECT url, mapkey FROM url_shortener.mapping
                WHERE url = %s;
            """,
            (url,)
        )
        result = cursor.fetchone()
        cursor.close()

        if result:
            return Mapping(url=result[0], mapkey=result[1])
        else:
            return None


    def search_mapkey(self, mapkey: str) -> Mapping|None:
        """ Search for a mapkey and retrieve the mapping if exists"""
        cursor = self.connection.driver.cursor()
        cursor.execute(
            """
                SELECT url, mapkey FROM url_shortener.mapping
                WHERE mapkey = %s;
            """,
            (mapkey,)
        )
        result = cursor.fetchone()
        cursor.close()
                
        if result:
            return Mapping(url=result[0], mapkey=result[1])
        else:
            return None
        

    def commit_mapping(self, mapping: Mapping) -> None:
        """ Commit a mapping to the database."""      
        cursor = self.connection.driver.cursor()
        cursor.execute(
            """
                INSERT INTO url_shortener.mapping (url, mapkey)
                VALUES (%s, %s);
            """,
            (mapping.url, mapping.mapkey)
        )
        cursor.close()
     

class CacheManager:
    """ Singleton cache manager"""

    def __new__(cls, cache_size: int) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(CacheManager, cls).__new__(cls)
        return cls.instance


    def __init__(self, cache_size: int) -> None:
        # Dict of Entry objects keyed by mapkey
        self.cache: dict[str, CacheManager.Entry] = dict()
        self.size = cache_size
    
    
    class Entry:
        """ Represents an entry in the cache"""
        def __init__(self, stamp: datetime, mapping: Mapping) -> None:
            self.stamp = stamp
            self.mapping = mapping


    def add(self, map: Mapping) -> None:
        if len(self.cache) < self.size:
            # If the cache isn't full add this entry
            self.cache[map.mapkey] = self.Entry(stamp=datetime.now(), mapping=map)
        else:
            # Replace the oldest entry in the cache
            minkey = list(self.cache.keys())[0]

            for key, value in self.cache.items():
                if value.stamp < self.cache[minkey].stamp:
                    minkey = key
            del self.cache[minkey]
            self.cache[map.mapkey] = self.Entry(stamp=datetime.now(), mapping=map)
            

    def search_mapkey(self, mapkey: str) -> Mapping|None:
        entry = self.cache.get(mapkey)
        if entry:
            # Update the last hit timestamp and return mapping
            self.cache[mapkey].stamp = datetime.now()
            return Mapping(url=entry.mapping.url, mapkey=entry.mapping.mapkey)
        else:
            return None
        

    def search_url(self, url: str) -> Mapping|None:
        for entry in self.cache.values():
            if entry.mapping.url == url:
                # Update the last hit timestamp and return mapping
                self.cache[entry.mapping.mapkey].stamp = datetime.now()
                return Mapping(url=entry.mapping.url, mapkey=entry.mapping.mapkey)
        return None

