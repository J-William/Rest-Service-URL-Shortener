import redis
from app.persistence import save_cache_mapping, search_cache_by_url, search_cache_by_shortcut

REDIS_HOST = 'redis'
REDIS_PORT = 6379

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


class TestCache:
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
        save_cache_mapping(
            url=TestCache.test_url,
            shortcut=TestCache.test_shortcut
        )

    def test_search_by_shortcut(self):
        res = search_cache_by_shortcut(TestCache.test_shortcut)

        assert res['_id'] == TestCache.test_shortcut

    def test_search_by_url(self):
        res = search_cache_by_url(TestCache.test_url)

        assert res['url'] == TestCache.test_url
