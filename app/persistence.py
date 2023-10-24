from pymongo.mongo_client import MongoClient
import redis
import os

MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT'))
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))

m_client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD
)
m_db = m_client['mapping-database']
m_col = m_db['mapping-collection']

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def search_db_by_url(url: str) -> dict | None:
    """ Search the db for a corresponding shortcut string given a url."""
    return m_col.find_one({'url': url})


def search_db_by_shortcut(shortcut: str) -> dict | None:
    """ Search the db for a corresponding url given a shortcut string."""
    return m_col.find_one({'_id': shortcut})


def search_cache_by_url(url: str) -> dict | None:
    """ Search the cache db for a corresponding shortcut string given a url."""
    res = r.hget('mapping-url', url)
    if res:
        return {
            '_id': res.decode('utf-8'),
            'url': url
        }
    else:
        return None


def search_cache_by_shortcut(shortcut: str):
    """ Search the cache for a corresponding yrl given a shortcut string."""
    res = r.hget('mapping-shortcut', shortcut)
    if res:
        return {
            '_id': shortcut,
            'url': res.decode('utf-8')
        }
    else:
        return None


def save_db_mapping(url: str, shortcut: str) -> None:
    """ Save a mapping to the database."""
    mapping = {'_id': shortcut, 'url': url}
    m_col.insert_one(mapping)


def save_cache_mapping(url: str, shortcut: str) -> None:
    """ Save a mapping to the cache."""
    r.hset('mapping-url', url, shortcut)
    r.hset('mapping-shortcut', shortcut, url)
