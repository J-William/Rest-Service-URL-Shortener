from app.models import Mapping
from pymongo.errors import DuplicateKeyError
import pytest


class TestMapping:
    test_mapping: Mapping

    @classmethod
    def setup_class(cls):
        cls.test_mapping = Mapping(url='https://www.abc.com/')

    @classmethod
    def teardown_class(cls):
        del cls.test_mapping

    def test_construction(self):
        assert TestMapping.test_mapping.url == 'https://www.abc.com/'

    def test_save(self):
        TestMapping.test_mapping.save()

    def test_find_url(self):
        mapping = Mapping.find(url=TestMapping.test_mapping.url)
        assert mapping.url == TestMapping.test_mapping.url

    def test_find_shortcut(self):
        mapping = Mapping.find(shortcut=TestMapping.test_mapping.shortcut)
        assert mapping.shortcut == TestMapping.test_mapping.shortcut

    def test_save_duplicate(self):
        """
            Assert that the DuplicateKeyError exception is raised
        """
        with pytest.raises(DuplicateKeyError):
            TestMapping.test_mapping.save()
