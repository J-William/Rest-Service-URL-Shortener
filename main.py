from fastapi import FastAPI
from models import MappingRequest

app = FastAPI()

@app.get("/")
async def root():
    # Test
    return {"message": "Hello World"}

@app.post('/p')
async def map(mapreq: MappingRequest):
    # Request a shortened url
    pass

@app.get('/g/{mapKey}')
async def getRedirect(mapKey):
    # Redirect to a mapped url
    pass

