from dataclasses import dataclass
from pydantic import HttpUrl
from models import Mapping
from datetime import datetime
import uuid
import psycopg2

@dataclass
class Connection:
    con_id : str
    driver : psycopg2.extensions.connection
    used : bool


class DatabaseConnectionManager():
    def __new__(cls, db_config: dict):
        """ Return a reference to the singleton class instance."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, db_config: dict):
        self.config = db_config
        self.pool = self.setup_pool()


    def get_driver(self):
        """ Get a psycopg2 connection to the database."""
        try:
            driver = psycopg2.connect(
                dbname = self.config['dbname'],
                user = self.config['user'],
                password = self.config['password'],
                port = self.config['port'],
                host = self.config['host']
            )
        except:
            raise 
        else:
            return driver
        

    def create_connection(self, used: bool = False) -> Connection:
        """ Connection creation method."""
        return Connection(
            con_id = uuid.uuid4().hex,
            driver = self.get_driver(),
            used = used
        )


    def setup_pool(self) -> list:
        """ Generate an initial pool of connections."""
        pool = list()
       
        for i in range(self.config['pool_min_size']):
            pool.append(self.create_connection())
        
        return pool


    def acquire(self) -> Connection:
        """ Acquire an unused connection."""
        # Return a connection from the pool if available
        for con in self.pool:
            if not con.used:
                con.used = True
                return con

        # If there is not one available create a new one if under the connection limit
        if len(self.pool) < self.config['pool_max_size']:
            new_con = self.create_connection(used=True)
            self.pool.append(new_con)
            return new_con
        else:
            return None


    def release(self, conn: Connection):
        """ Release a connection."""
        self.pool[self.pool.index(conn)].used = False

    

class DatabaseManager():
    """ Db interface """
    def __init__(self, cm: DatabaseConnectionManager):
        self.cm = cm
        # Reference to the Connection object
        self.connection = self.cm.acquire()


    def teardown(self):
        self.cm.release(self.connection)
        
    def search_mapping_url(self, original_url: HttpUrl) -> Mapping|None:
        cursor = self.connection.driver.cursor()
        cursor.execute(""" 
                SELECT * FROM url_shortener.mapping
                WHERE original_url = %s;
            """,
            (original_url,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result

    def search_mapping_mapkey(self, mapkey: str) -> Mapping|None:
        cursor = self.connection.driver.cursor()
        cursor.execute(
            """
                SELECT original_url, mapkey FROM url_shortener.mapping
                WHERE mapkey = %s;
            """,
            (mapkey,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result


    def commit_mapping(self, mapping: Mapping):
        """ Commit a mapping to the database."""
        cursor = self.connection.driver.cursor()
        cursor.execute(
            """
                INSERT INTO url_shortener.mapping (original_url, mapkey)
                VALUES (%s, %s);
            """,
            (mapping.original_url, mapping.mapkey)
        )
        cursor.close()
        self.connection.commit()



class CacheManager:
    def __new__(cls, cache_size: int):
        """ Return a reference to the singleton class instance."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(CacheManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, cache_size: int):
        self.cache = dict()
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
            

    def search(self, mapkey: str) -> Mapping|None:
        return self.cache.get(mapkey)


