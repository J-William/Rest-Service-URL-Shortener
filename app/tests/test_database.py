from app.database import DatabaseConnectionManager
import json


TEST_CONFIG_FILE = 'config/test_config.json'

with open(TEST_CONFIG_FILE) as f:
    TEST_CONFIG = json.loads(f.read())




class TestDatabase:
    @classmethod
    def setup_class(cls):
        global dbcm
        dbcm = DatabaseConnectionManager(TEST_CONFIG)

    @classmethod
    def teardown_class(cls):
        global dbcm
        dbcm.teardown()
        del dbcm

    def test_acquire_connection(self):
        conn = dbcm.acquire()
        assert conn.driver.closed == 0
        dbcm.release(conn)
        
    def test_query(self):
        conn = dbcm.acquire()
        cursor = conn.driver.cursor()
        cursor.execute("""SELECT 'X';""")
        assert cursor.fetchone()[0] == 'X'
        cursor.close()
        dbcm.release(conn)


