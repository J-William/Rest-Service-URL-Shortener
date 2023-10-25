from typing import Any
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from app.models import MappingRequest, Mapping
from pymongo.errors import DuplicateKeyError

app = FastAPI()


@app.get('/')
async def service_status(response: Response) -> Any:
    """ Test the service """
    return {"msg": "Url Shortener v1.7 Service Available"}


@app.post('/api/v1/shorten')
async def shorten_url(mapreq: MappingRequest, response: Response) -> Any:
    """Request a shortened url mapping"""

    new_mapping = Mapping(url=str(mapreq.url))

    try:
        new_mapping.save()
    except DuplicateKeyError:   # If the Mapping already exists just return it
        existing_mapping = Mapping.find(url=str(mapreq.url))
        return {"message": "Already exists", "shortcut": existing_mapping.shortcut}

    response.status_code = status.HTTP_201_CREATED
    return {"message": "Success", "shortcut": new_mapping.shortcut}


@app.get('/api/v1/{shortcut}')
async def get_redirect(shortcut: str) -> Any:
    """Redirect to a mapped url"""
    mapping = Mapping.find(shortcut=shortcut)

    if mapping:
        return RedirectResponse(mapping.url, status_code=status.HTTP_308_PERMANENT_REDIRECT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")


