from fastapi import FastAPI, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from models import MappingRequest, Mapping
from persistence import MappingPersistenceManager, CacheManager
from utilities import generate_mapkey
import json


app = FastAPI()

with open('config.json') as f:
    config = json.loads(f.read())

# DAO convenience constructor
get_db = lambda : MappingPersistenceManager(db_config=config)

cache = CacheManager(cache_size=config['cache_size'])


@app.post('/api/v1/data/shorten', status_code=status.HTTP_201_CREATED)
async def map(mapreq: MappingRequest, response: Response):
    """Request a shortened url mapping"""
    db = get_db()

    map = cache.search_url(mapreq.url) or db.search_url(mapreq.url)

    if map:
        # Return failure resource already exists
        response.status_code = status.HTTP_403_FORBIDDEN
        db.teardown()
        return "Error, mapping already exists"
    else:
        # Create a new mapping
        mapkey = generate_mapkey()

        # If there is a collision generate new mapkeys until there isn't
        while cache.search_mapkey(mapkey) or db.search_mapkey(mapkey):
            mapkey = generate_mapkey()

        map = Mapping(mapreq.url, mapkey)

        # Commit the mapping
        db.commit_mapping(map)
        
        db.teardown()
        
        return "Success"
    
    

@app.get('/api/v1/{mapkey}')
async def getRedirect(mapkey):
    """Redirect to a mapped url"""
    map = cache.search_mapkey(mapkey)

    if not map:
        db = get_db()
        map = db.search_mapkey(mapkey)
        db.teardown()

    if not map:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    else:
        # Client network error during testing redirects probably CORS issue
        # return RedirectResponse(map.url)
        return {"message": f"you were redirected to {map.url}"}


