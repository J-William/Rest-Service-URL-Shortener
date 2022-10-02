from pydantic import HttpUrl, PostgresDsn
from models import Mapping
import psycopg2

class ConnectionManager():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, db_config: dict):
        self.config = db_config

    def get_conn(self):
        try:
            connection = psycopg2.connect(
                dbname = self.config['dbname'],
                user = self.config['user'],
                password = self.config['password'],
                port = self.config['port'],
                host = self.config['host']
            )
        except:
            pass

        return None


class PersistenceManager():
    """ Db interface """
    def __init__(self, dbcm: ConnectionManager):
        self.connection = dbcm.get_conn()

    def search_mapping(self, uid: int = None, ourl: HttpUrl = None, mapKey: str = None)  -> Mapping|None:
        """ Search the database for a mapping based on one or more attributes; return None if not found."""
        pass


    def commit_mapping(self, mapping: Mapping):
        """ Commit a mapping to the database."""
        pass

