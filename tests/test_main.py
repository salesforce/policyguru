import unittest
from starlette.testclient import TestClient

from policyguru.main import app

client = TestClient(app)


class TestMain(unittest.TestCase):
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}
