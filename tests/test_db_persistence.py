from pymongo.mongo_client import MongoClient
from pydantic import HttpUrl

from app.persistence import save_db_mapping, search_db_by_shortcut, search_db_by_url

MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_USERNAME = 'root'
MONGO_PASSWORD = 'examplePassword'

m_client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD
)
m_db = m_client['mapping-database']
m_col = m_db['mapping-collection']


class TestDbPersistence:
    test_shortcut = None
    test_url = None

    @classmethod
    def setup_class(cls):
        cls.test_url = 'https://www.abc.com/'
        cls.test_shortcut = 'abc123'

    @classmethod
    def teardown_class(cls):
        del cls.test_url
        del cls.test_shortcut

    def test_new_save(self):
        save_db_mapping(url=HttpUrl(TestDbPersistence.test_url), shortcut='abc123')

    def test_search_by_shortcut(self):
        res = search_db_by_shortcut(shortcut=TestDbPersistence.test_shortcut)

        assert res['_id'] == TestDbPersistence.test_shortcut

    def test_search_by_url(self):
        res = search_db_by_url(url=HttpUrl(TestDbPersistence.test_url))

        assert res['url'] == TestDbPersistence.test_url
