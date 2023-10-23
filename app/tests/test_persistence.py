from app.persistence import CacheManager, MappingPersistenceManager
from app.database import DatabaseConnectionManager
from app.models import Mapping
from app.utilities import generate_mapkey, ALPHABET
import time
import random
import json


CONFIG_FILE = 'config/config.json'

with open(CONFIG_FILE) as f:
    CONFIG = json.loads(f.read())


def generate_random_mapping():
    random_string = ''.join(random.choices(ALPHABET, k=8))
    return Mapping(f'http://www.{random_string}.com', generate_mapkey())


class TestMappingPersistenceManager:
    @classmethod
    def setup_class(cls):
        global dbcm, db, mapping
        dbcm = DatabaseConnectionManager(CONFIG)
        db = MappingPersistenceManager(dbcm=dbcm)
        mapping = generate_random_mapping()

    @classmethod
    def teardown_class(cls):
        global dbcm, db, mapping
        db.teardown()
        dbcm.teardown()
        del db, dbcm, mapping

    def test_initialization(self):
        assert db.connection.driver.closed == 0
        assert db.connection.driver.autocommit == True
        
    def test_commit_mapping(self):
        db.commit_mapping(mapping)
        

    def test_url_search(self):
        map = db.search_url(mapping.url)
        assert map.mapkey == mapping.mapkey

    def test_mapkey_search(self):
        map = db.search_mapkey(mapping.mapkey)
        assert map.url == mapping.url


        

class TestCacheManager:
    @classmethod
    def setup_class(cls):
        global cm, mapping
        cm = CacheManager(CONFIG['cache_size'])
        mapping = generate_random_mapping()
    
    @classmethod
    def teardown_class(cls):
        global cm, mapping
        del cm, mapping

    def test_basic_add(self):
        cm.add(mapping)
        mappings = list()
        for entry in cm.cache.values():
            mappings.append(entry.mapping)
        assert mapping in mappings

    def test_search_mapkey(self, cache):
        map = cm.search_mapkey(mapping.mapkey)
        assert map.url == mapping.url

    def test_search_url(self):
        map = cm.search_url(mapping.url)
        assert map.mapkey == mapping.mapkey

    def test_size_limit(self):
        for _ in range(CONFIG['cache_size'] + 5):
            cm.add(generate_random_mapping())

        assert len(cm.cache) <= CONFIG['cache_size']


    def test_lru_logic(self):
        for _ in range(CONFIG['cache_size']):
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
        




    
