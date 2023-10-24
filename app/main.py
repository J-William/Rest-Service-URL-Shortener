from typing import Any
from fastapi import FastAPI, Response, HTTPException, status
# from fastapi.responses import RedirectResponse
# from app.models import MappingRequest, Mapping
# from app.utilities import generate_shortcut
# import json

app = FastAPI()


# Load config


@app.get('/')
async def service_status(response: Response) -> Any:
    """ Test the service """
    return {"msg": "Url Shortener v1.7 Service Available"}
#
#
# @app.post('/api/v1/shorten', status_code=status.HTTP_201_CREATED)
# async def shorten_url(mapreq: MappingRequest, response: Response) -> Any:
#     """Request a shortened url mapping"""
#     db = get_db()
#
#     map = cache.search_url(mapreq.url) or db.search_url(mapreq.url)
#
#     if map:
#         # Return failure resource already exists
#         response.status_code = status.HTTP_403_FORBIDDEN
#         db.teardown()
#         return "Error, mapping already exists"
#     else:
#         # Create a new mapping
#         mapkey = generate_mapkey()
#
#         # If there is a collision generate new mapkeys until there isn't
#         while cache.search_mapkey(mapkey) or db.search_mapkey(mapkey):
#             mapkey = generate_mapkey()
#
#         map = Mapping(mapreq.url, mapkey)
#
#         # Commit the mapping
#         db.commit_mapping(map)
#
#         db.teardown()
#
#         return {"message": "Success", "mapkey": mapkey}
#
#
#
# @app.get('/api/v1/{mapkey}')
# async def get_redirect(mapkey: str) -> Any:
#     """Redirect to a mapped url"""
#     map = cache.search_mapkey(mapkey)
#
#     if not map:
#         db = get_db()
#         map = db.search_mapkey(mapkey)
#         db.teardown()
#
#     if not map:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL not found")
#     else:
#         # Client network error during testing redirects; probably CORS issue
#         #return RedirectResponse(map.url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
#         return {"message": f"You were redirected to {map.url}"}
