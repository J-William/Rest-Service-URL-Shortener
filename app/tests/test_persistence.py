from app.persistence import CacheManager, MappingPersistenceManager
from app.models import Mapping
from app.utilities import generate_mapkey, ALPHABET
import time
import psycopg2
import random
import json


TEST_CONFIG_FILE = 'config/test_config.json'
TEST_URL = 'http://www.test.com'
TEST_MAPKEY = '000000'

with open(TEST_CONFIG_FILE) as f:
    TEST_CONFIG = json.loads(f.read())



def generate_random_mapping():
    random_string = ''.join(random.choices(ALPHABET, k=8))
    return Mapping('http://www.{random_string}.com', generate_mapkey())


#### Database Connection

class ConnectionManager:
    def __init__(self, config) -> None:
        self.connection = psycopg2.connect(
                dbname = config['dbname'],
                user = config['user'],
                password = config['password'],
                port = config['port'],
                host = config['host']
            )
        
        self.connection.set_session(autocommit=True)



class TestDatabase:
    @classmethod
    def setup_class(cls):
        global cm
        cm = ConnectionManager(TEST_CONFIG)

    @classmethod
    def teardown_class(cls):
        cm.connection.close()

    def test_connection(self):
        assert cm.connection.closed == 0
        
    def test_query(self):
        cursor = cm.connection.cursor()
        cursor.execute("""SELECT 'X';""")
        assert cursor.fetchone()[0] == 'X'
        cursor.close()



### MappingPersistenceManager DAO



class TestMappingPersistenceManager:
    @classmethod
    def setup_class(cls):
        global db
        db = MappingPersistenceManager(TEST_CONFIG)

    @classmethod
    def teardown_class(cls):
        db.teardown()

    def test_initialization(self):
        assert db.connection.closed == 0
        assert db.connection.autocommit == True
        
    def test_url_search(self):
        map = db.search_url(TEST_URL)
        assert map.mapkey == TEST_MAPKEY

    def test_mapkey_search(self):
        map = db.search_mapkey(TEST_MAPKEY)
        assert map.url == TEST_URL

    def test_commit_mapping(self):
        map = Mapping(TEST_URL, TEST_MAPKEY)

### CacheManager

class TestCacheManager:
    @classmethod
    def setup_class(cls):
        global cache 
        cache = CacheManager(TEST_CONFIG['cache_size'])
    
    def test_basic_add(self):
        map = Mapping(TEST_URL, TEST_MAPKEY)
        cache.add(map)
        mappings = list()
        for entry in cache.cache.values():
            mappings.append(entry.mapping)
        assert map in mappings

    def test_search_mapkey(self):
        map = cache.search_mapkey(TEST_MAPKEY)
        assert map.url == TEST_URL

    def test_search_url(self):
        map = cache.search_url(TEST_URL)
        assert map.mapkey == TEST_MAPKEY

    def test_size_limit(self):
        for _ in range(TEST_CONFIG['cache_size'] + 5):
            cache.add(generate_random_mapping())

        assert len(cache.cache) <= TEST_CONFIG['cache_size']


    def test_lru_logic(self):
        for _ in range(TEST_CONFIG['cache_size']):
            cache.add(generate_random_mapping())
            time.sleep(0.01)

        # Find the oldest entry
        minkey = list(cache.cache.keys())[0]
        minstamp = cache.cache[minkey].stamp    

        for key, entry in cache.cache.items():
            if entry.stamp < minstamp:
                minkey = key
                minstamp = entry.stamp

        map = generate_random_mapping()
        # Add another entry
        cache.add(map)

        # The oldest entry should have been replaced by the new one
        assert minkey not in cache.cache.keys()
        assert map.mapkey in cache.cache.keys()
        




    
