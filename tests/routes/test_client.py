import unittest
from unittest.mock import patch

import mongomock
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect

from app.models.user import User
from tests.conftest import redis_client


class TestClientRoute(unittest.TestCase):
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
            fake_token = self.get_fake_token()
            self.headers = {"Authorization": f"Bearer {fake_token}"}

    def tearDown(self) -> None:
        disconnect()

    def get_fake_token(self):
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
            fake_token = response.json()["access_token"]
            return fake_token

    def test_create_client(self):
        with patch(
            "app.repositories.client_repository.ClientRepository.create_client"
        ) as mock_create_client:
            mock_create_client.return_value = {
                "name": "Client Test",
                "email": "client@gmail.com",
                "favorites": [],
            }

            response = self.client.post(
                "/clients/",
                params={"name": "Client Test", "email": "client@gmail.com"},
                headers=self.headers,
            )
            assert response.status_code == 200
            assert response.json()["name"] == "Client Test"

    def test_update_client(self):
        with patch(
            "app.repositories.client_repository.ClientRepository.update_client"
        ) as mock_update_client:
            mock_update_client.return_value = {
                "name": "Updated Client",
                "email": "updated@gmail.com",
                "favorites": [],
            }

            response = self.client.put(
                "/clients/123",
                json={"name": "Updated Client", "email": "updated@gmail.com"},
                headers=self.headers,
            )
            assert response.status_code == 200
            assert response.json()["name"] == "Updated Client"

    def test_delete_client(self):
        with patch(
            "app.repositories.client_repository.ClientRepository.delete_client"
        ) as mock_delete_client:
            mock_delete_client.return_value = {"message": "Client deleted"}

            response = self.client.delete("/clients/123", headers=self.headers)
            assert response.status_code == 200
            assert response.json()["message"] == "Client deleted"


if __name__ == "__main__":
    unittest.main()
