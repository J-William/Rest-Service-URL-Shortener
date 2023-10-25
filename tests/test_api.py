from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.utilities import ALPHABET
import random

client = TestClient(app)


def generate_random_url(length: int) -> str:
    random_string = ''.join(random.choices(ALPHABET, k=length))
    return f'http://www.{random_string.lower()}.com'


class TestApi:
    shortcut = None
    test_url = None

    @classmethod
    def setup_class(cls):
        cls.test_url = generate_random_url(5)

    def test_read_status(self):
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"msg": "Url Shortener v1.7 Service Available"}

    def test_shorten_url(self):
        response = client.post(
            "/api/v1/shorten",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={"url": TestApi.test_url}
        )
        res = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        TestApi.shortcut = res['shortcut']

    def test_get_redirect(self):
        response = client.get(f"/api/v1/{TestApi.shortcut}", allow_redirects=False)
        assert response.status_code == status.HTTP_308_PERMANENT_REDIRECT
        assert TestApi.test_url in response.headers['location']
