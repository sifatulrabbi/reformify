if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestLoginRoute(unittest.TestCase):
    def test_with_correct_payload(self):
        payload = {
            "email": "test.user@sifatulrabbi.com",
            "password": "password",
        }
        res = client.post("/auth/login", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data is not None
        user = data.get("user")
        assert user is not None
        assert user.get("email") == payload["email"]
        assert data.get("access_token") is not None

    def test_with_incorrect_password(self):
        payload = {
            "email": "test.user@sifatulrabbi.com",
            "password": "short",
        }
        res = client.post("/auth/login", json=payload)
        assert res.status_code == 401
        data = res.json()
        assert data is not None
        assert isinstance(data.get("message"), str)

    def test_with_incorrect_email(self):
        self.skipTest("Need to implement email validation")
        payload = {
            "email": "test.user@sifatulrabbi.com",
            "password": "password",
        }
        res = client.post("/auth/login", json=payload)
        assert res.status_code == 401
        data = res.json()
        assert data is not None
        assert isinstance(data.get("message"), str)

class TestRegisterRoute(unittest.TestCase):
    def test_with_correct_payload(self):
        payload = {
            "email": "test.user@sifatulrabbi.com",
            "password": "password",
            "fullname": "Sifatul rabbi",
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 201
        data = res.json()
        assert data is not None
        user = data.get("user")
        assert user is not None
        assert user.get("email") == payload["email"]
        assert user.get("fullname") == payload["fullname"]
        assert data.get("access_token") is not None

    def test_with_incorrect_password(self):
        payload = {
            "email": "test.user@sifatulrabbi.com",
            "password": "short",
            "fullname": "Sifatul rabbi",
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 400
        data = res.json()
        assert data is not None
        assert isinstance(data.get("message"), str)

    def test_with_incorrect_fullname(self):
        payload = {
            "email": "test.user@sifatulrabbi.com",
            "password": "short",
            "fullname": "",
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 400
        data = res.json()
        assert data is not None
        assert isinstance(data.get("message"), str)

    def test_with_existing_user(self):
        payload = {
            "email": "test.user@sifatulrabbi.com",
            "password": "short",
            "fullname": "Sifatul Rabbi",
        }
        res = client.post("/auth/register", json=payload)
        assert res.status_code == 409
        data = res.json()
        assert data is not None
        assert isinstance(data.get("message"), str)

    def test_with_incorrect_email(self):
        self.skipTest("Need to implement email validation")
        payload = {
            "email": "test.sifatulrabbi.com",
            "password": "password",
            "fullname": "Sifatul rabbi",
        }
        res = client.post("/auth/login", json=payload)
        assert res.status_code == 400
        data = res.json()
        assert data is not None
        assert isinstance(data.get("message"), str)

if __name__ == "__main__":
    unittest.main(defaultTest="TestLoginRoute")
