import uuid
import psycopg2 # type: ignore
import time
from dataclasses import dataclass
from typing import Any
from app.exceptions import DatabaseUnavailable, ConnectionTimeout


@dataclass
class Connection:
    con_id : str
    driver : Any
    used : bool


class DatabaseConnectionManager():
    """ Singleton connection manager to administer the pool of db connections"""
    
    def __new__(cls, db_config: dict):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseConnectionManager, cls).__new__(cls)
        return cls.instance


    def __init__(self, db_config: dict) -> None:
        self.config = db_config
        self.pool = self.setup_pool()
        self.acquire_wait_time = self.config['acquire_wait_time']
        self.acquire_wait_timeout = self.config['acquire_wait_timeout']


    def teardown(self) -> None:
        for conn in self.pool:
            conn.driver.close()
            del conn
            

    def get_driver(self) -> Any:
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
            raise DatabaseUnavailable('Failed to creation connection.')

        # Autocommit DML 
        driver.set_session(autocommit=True)
        return driver       
        

    def create_connection(self, used: bool = False) -> Connection:
        return Connection(
            con_id = uuid.uuid4().hex,
            driver = self.get_driver(),
            used = used
        )


    def setup_pool(self) -> list[Connection]:
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
            # Else wait a little while and try again
            waited = float()
            while(True):
                time.sleep(self.acquire_wait_time)
                waited += .01
                for con in self.pool:
                    if not con.used:
                        con.used = True
                        return con

                if waited > self.acquire_wait_timeout:
                    raise ConnectionTimeout('Timed out waiting for a DB connection.')


    def release(self, conn: Connection) -> None:
        """ Release a connection."""
        self.pool[self.pool.index(conn)].used = False
