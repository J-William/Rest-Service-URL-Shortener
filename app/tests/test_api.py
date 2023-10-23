from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.utilities import ALPHABET
import random
import os


client = TestClient(app)

def generate_random_url(length: int) -> str:
    random_string = ''.join(random.choices(ALPHABET, k= length))
    return f'http://www.{random_string}.com'


test_url = generate_random_url(10)
test_mapkey = str()

def test_read_status():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "Url Shortener v1.0 Service Available"}


def test_shorten_url():
    response = client.post(
        "/api/v1/shorten",
        headers={ "accept": "application/json", "Content-Type": "application/json" },
        json= { "url": test_url }
        )

    res = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    # Capture to use in the next test
    global test_mapkey
    test_mapkey = res["mapkey"]
    
    assert res["message"] == "Success"
    assert len(res["mapkey"]) <= 8
    
    for char in  res["mapkey"]:
        assert char in ALPHABET

    

def test_get_redirect():    
    response = client.get(f"/api/v1/{test_mapkey}")

    res = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert test_url in res["message"]

