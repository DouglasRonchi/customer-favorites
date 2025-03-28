import unittest
from unittest.mock import patch

import mongomock
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect

from app.models.user import User
from tests.conftest import redis_client


class TestAuthRoute(unittest.TestCase):
    def setUp(self) -> None:
        disconnect()
        with patch(
            "app.database.database.MongoDBConnection._set_connection"
        ) as mock_connection:
            mock_connection.return_value = None
            connect(
                "mongoenginetest",
                mongo_client_class=mongomock.MongoClient,
                uuidRepresentation="standard",
            )
        with patch("app.database.cache.RedisClient.connect") as mock_connect:
            mock_connect.return_value = None
            from app.main import app

            self.client = TestClient(app)
            self.redis_client = redis_client

    def tearDown(self) -> None:
        disconnect()

    def test_register_user(self):
        with patch("app.models.user.User.objects") as mock_objects:
            mock_objects.return_value.first.return_value = None
            mock_user = User(
                email="test@gmail.com", name="Test User", password="testpass"
            )
            mock_user.save = None
            mock_objects.return_value.create.return_value = mock_user

            response = self.client.post(
                "/register",
                json={
                    "email": "test@gmail.com",
                    "name": "Test User",
                    "password": "testpass",
                },
            )
            assert response.status_code == 200
            assert "access_token" in response.json()

    def test_register_existing_user(self):
        with patch("app.models.user.User.objects") as mock_objects:
            mock_objects.return_value.first.return_value = User(
                email="test@gmail.com", name="Test User", password="testpass"
            )

            response = self.client.post(
                "/register",
                json={
                    "email": "test@gmail.com",
                    "name": "Test User",
                    "password": "testpass",
                },
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "E-mail already registered"

    def test_login_success(self):
        with patch("app.models.user.User.objects") as mock_objects:
            mock_objects.return_value.first.return_value = User(
                email="test@gmail.com", password="testpass"
            )

            response = self.client.post(
                "/login",
                json={
                    "email": "test@gmail.com",
                    "password": "testpass",
                    "name": "Test User",
                },
            )
            assert response.status_code == 200
            assert "access_token" in response.json()

    def test_login_invalid_credentials(self):
        with patch("app.models.user.User.objects") as mock_objects:
            mock_objects.return_value.first.return_value = None

            response = self.client.post(
                "/login",
                json={
                    "email": "invalid@gmail.com",
                    "password": "invalidpass",
                    "name": "Test User",
                },
            )
            assert response.status_code == 401
            assert response.json()["detail"] == "401: Invalid credentials"


if __name__ == "__main__":
    unittest.main()
