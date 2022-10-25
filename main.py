from fastapi import FastAPI
from models import MappingRequest, Mapping
from persistence import DatabaseConnectionManager, DatabaseManager, CacheManager
import json

app = FastAPI()

# TODO configuration
with open('config.json') as f:
    config = json.loads(f.read())

# Singleton connection manager
dbcm = DatabaseConnectionManager(db_config=config)

# DatbaseManager convenience constructor
get_db = lambda : DatabaseManager(cm=dbcm)

cache = CacheManager(cache_size=config['cache_size'])


@app.post('/p')
async def map(mapreq: MappingRequest):
    # Request a shortened url
    db = get_db()

    map = db.search_mapping_url(mapreq.original_url)

    if map:
        # Return failure resource already exists
        return "Error, resource already exists"
    else:
        map = Mapping(url=mapreq.original_url)

        # If there is a collision generate new mapkeys until there isn't
        while cache.search(mapkey=map.mapkey) or db.search_mapping_mapkey(mapkey=map.mapkey):
            map = Mapping(url=mapreq.original_url)

        
        try:
            # Commit the mapping
            db.commit_mapping(mapping=map)
        except:
            return "Error, database transaction failure."
        finally:
            db.teardown()
        
        return "Success"
    

@app.get('/g/{mapkey}')
async def getRedirect(mapkey):
    # Redirect to a mapped url
    map = cache.search(mapkey=mapkey)

    if not map:
        db = get_db()
        map = db.search_mapping_mapkey(mapkey=mapkey)
        db.teardown()

    if not map:
        return "Error, url not found."
    else:
        return "Redirect to map.original_url"
