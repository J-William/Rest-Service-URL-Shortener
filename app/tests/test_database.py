from app.database import DatabaseConnectionManager
import json


CONFIG_FILE = 'config/config.json'

with open(CONFIG_FILE) as f:
    CONFIG = json.loads(f.read())




class TestDatabase:
    @classmethod
    def setup_class(cls):
        global dbcm
        dbcm = DatabaseConnectionManager(CONFIG)

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

    def test_pool_min(self):
        assert len(dbcm.pool) == CONFIG['pool_min_size']
    
    def test_pool_max(self):
        conns = list()
        for i in range(CONFIG['pool_max_size']):
            conns.append(dbcm.acquire())

        assert len(dbcm.pool) == CONFIG['pool_max_size']

        for conn in conns:
            dbcm.release(conn)

    
    

