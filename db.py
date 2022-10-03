from dataclasses import dataclass
from pydantic import HttpUrl
from models import Mapping
import uuid
import psycopg2

@dataclass
class Connection:
    con_id : str
    driver : psycopg2.extensions.connection
    used : bool


class ConnectionManager():
    def __new__(cls, db_config:dict):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConnectionManager, cls).__new__(cls)
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
    def __init__(self, dbcm: ConnectionManager):
        self.dbcm = dbcm
        # Reference to the Connection object
        self.connection = dbcm.acquire()


    def teardown(self):
        self.dbcm.release(self.connection)
        
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

    def search_mapping_mapkey(self, mapKey: str) -> Mapping|None:
        cursor = self.connection.driver.cursor()
        cursor.execute(
            """
                SELECT original_url, mapkey FROM url_shortener.mapping
                WHERE mapkey = %s;
            """,
            (mapKey,)
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
            (mapping.original_url, mapping.mapKey)
        )
        cursor.close()
        self.connection.commit()


