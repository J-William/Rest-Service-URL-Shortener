from dataclasses import dataclass
from pydantic import HttpUrl
from models import Mapping
from datetime import datetime
import psycopg2 # type: ignore


class MappingPersistenceManager():
    """ Db interface """
    def __init__(self, db_config: dict):
        self.config = db_config

        self.connection = psycopg2.connect(
                dbname = self.config['dbname'],
                user = self.config['user'],
                password = self.config['password'],
                port = self.config['port'],
                host = self.config['host']
            )
        
        self.connection.set_session(autocommit=True)

    def __del__(self):
        self.teardown()

    def teardown(self):
        self.connection.close()
        
    def search_url(self, url: HttpUrl) -> Mapping|None:
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
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
        

    def commit_mapping(self, mapping: Mapping):
        """ Commit a mapping to the database."""
        cursor = self.connection.cursor()
        cursor.execute(
            """
                INSERT INTO url_shortener.mapping (url, mapkey)
                VALUES (%s, %s);
            """,
            (mapping.url, mapping.mapkey)
        )
        self.connection.commit()
        cursor.close()



class CacheManager:
    def __new__(cls, cache_size: int):
        """ Return a reference to the singleton class instance."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(CacheManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, cache_size: int):
        # Dict of Entry objects keyed by mapkey
        self.cache: dict[str, CacheManager.Entry] = dict()
        self.size = cache_size
    
    @dataclass(frozen=True)
    class Entry:
        stamp : datetime
        mapping : Mapping    


    def add(self, map: Mapping):
        if len(self.cache) < self.size:
            # If the cache isn't full add this entry
            self.cache[map.mapkey] = self.Entry(stamp=datetime.now(), mapping=map)
        else:
            # Replace the oldest entry in the cache
            minkey = list(self.cache.keys())[0]

            for key, value in self.cache.items():
                if value.stamp < self.cache[minkey].stamp:
                    minkey = key
            
            self.cache[minkey] = self.Entry(stamp=datetime.now(), mapping=map)
            

    def search_mapkey(self, mapkey: str) -> Mapping|None:
        entry = self.cache.get(mapkey)
        if entry:
            return Mapping(url=entry.mapping.url, mapkey=entry.mapping.mapkey)
        else:
            return None
        

    def search_url(self, url: str) -> Mapping|None:
        for entry in self.cache.values():
            if entry.mapping.url == url:
                return Mapping(url=entry.mapping.url, mapkey=entry.mapping.mapkey)
        return None

