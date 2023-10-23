from pymongo.mongo_client import MongoClient
from pydantic import HttpUrl
import redis

MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_USERNAME = 'root'
MONGO_PASSWORD = 'examplePassword'

REDIS_HOST = 'redis'
REDIS_PORT = 6379

m_client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD
)
m_db = m_client['mapping-database']
m_col = m_db['mapping-collection']

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def search_db_by_url(url: HttpUrl) -> dict | None:
    """ Search the db for a corresponding shortcut string given a url."""
    return m_col.find_one({'url': str(url)})


def search_db_by_shortcut(shortcut: str) -> dict | None:
    """ Search the db for a corresponding url given a shortcut string."""
    return m_col.find_one({'_id': shortcut})


def search_cache_by_url(url: HttpUrl):
    """ Search the cache db for a corresponding shortcut string given a url."""
    pass


def search_cache_by_shortcut(shortcut: str):
    """ Search the cache for a corresponding yrl given a shortcut string."""
    pass


def save_db_mapping(url: HttpUrl, shortcut: str) -> None:
    """ Save a mapping to the database."""
    mapping = {'_id': shortcut, 'url': str(url)}
    m_col.insert_one(mapping)


def save_cache_mapping(url: HttpUrl, shortcut: str):
    """ Save a mapping to the cache."""
    pass
