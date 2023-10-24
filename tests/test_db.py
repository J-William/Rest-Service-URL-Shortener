from pymongo.mongo_client import MongoClient
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


class TestDb:
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
        save_db_mapping(
            url=TestDb.test_url,
            shortcut=TestDb.test_shortcut
        )

    def test_search_by_shortcut(self):
        res = search_db_by_shortcut(shortcut=TestDb.test_shortcut)

        assert res['_id'] == TestDb.test_shortcut

    def test_search_by_url(self):
        res = search_db_by_url(url=TestDb.test_url)

        assert res['url'] == TestDb.test_url
