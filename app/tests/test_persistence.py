from app.persistence import CacheManager, MappingPersistenceManager
from app.database import DatabaseConnectionManager
from app.models import Mapping
from app.utilities import generate_mapkey, ALPHABET
import time
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


class TestMappingPersistenceManager:
    @classmethod
    def setup_class(cls):
        global dbcm, db
        dbcm = DatabaseConnectionManager(TEST_CONFIG)
        db = MappingPersistenceManager(dbcm=dbcm)

    @classmethod
    def teardown_class(cls):
        global dbcm, db
        db.teardown()
        dbcm.teardown()
        del db, dbcm

    def test_initialization(self):
        assert db.connection.driver.closed == 0
        assert db.connection.driver.autocommit == True
        
    def test_url_search(self):
        map = db.search_url(TEST_URL)
        assert map.mapkey == TEST_MAPKEY

    def test_mapkey_search(self):
        map = db.search_mapkey(TEST_MAPKEY)
        assert map.url == TEST_URL

    def test_commit_mapping(self):
        map = Mapping(TEST_URL, TEST_MAPKEY)
        

class TestCacheManager:
    @classmethod
    def setup_class(cls):
        global cm
        cm = CacheManager(TEST_CONFIG['cache_size'])
    
    @classmethod
    def teardown_class(cls):
        global cm
        del cm

    def test_basic_add(self):
        map = Mapping(TEST_URL, TEST_MAPKEY)
        cm.add(map)
        mappings = list()
        for entry in cm.cache.values():
            mappings.append(entry.mapping)
        assert map in mappings

    def test_search_mapkey(self, cache):
        map = cm.search_mapkey(TEST_MAPKEY)
        assert map.url == TEST_URL

    def test_search_url(self):
        map = cm.search_url(TEST_URL)
        assert map.mapkey == TEST_MAPKEY

    def test_size_limit(self):
        for _ in range(TEST_CONFIG['cache_size'] + 5):
            cm.add(generate_random_mapping())

        assert len(cm.cache) <= TEST_CONFIG['cache_size']


    def test_lru_logic(self):
        for _ in range(TEST_CONFIG['cache_size']):
            cm.add(generate_random_mapping())
            time.sleep(0.01)

        # Find the oldest entry
        minkey = list(cm.cache.keys())[0]
        minstamp = cm.cache[minkey].stamp    

        for key, entry in cm.cache.items():
            if entry.stamp < minstamp:
                minkey = key
                minstamp = entry.stamp

        map = generate_random_mapping()
        # Add another entry
        cm.add(map)

        # The oldest entry should have been replaced by the new one
        assert minkey not in cm.cache.keys()
        assert map.mapkey in cm.cache.keys()
        




    
