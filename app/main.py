from typing import Any
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from app.models import MappingRequest, Mapping

app = FastAPI()


# Load config


@app.get('/')
async def service_status(response: Response) -> Any:
    """ Test the service """
    return {"msg": "Url Shortener v1.7 Service Available"}


@app.post('/api/v1/shorten', status_code=status.HTTP_201_CREATED)
async def shorten_url(mapreq: MappingRequest) -> Any:
    """Request a shortened url mapping"""

    existing_mapping = Mapping.find(url=str(mapreq.url))

    if existing_mapping:
        # Return failure resource already exists
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mapping already exists."
        )
    else:
        # Create a new mapping
        new_mapping = Mapping(url=str(mapreq.url))

        # Persist the new mapping
        new_mapping.save()

        return {"message": "Success", "shortcut": new_mapping.shortcut}


@app.get('/api/v1/{shortcut}')
async def get_redirect(shortcut: str) -> Any:
    """Redirect to a mapped url"""
    mapping = Mapping.find(shortcut=shortcut)

    if not mapping:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL not found")
    else:
        # Client network error during testing redirects; probably CORS issue
        return RedirectResponse(mapping.url, status_code=status.HTTP_308_PERMANENT_REDIRECT)
