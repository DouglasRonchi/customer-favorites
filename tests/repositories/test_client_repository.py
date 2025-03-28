import unittest
from unittest.mock import MagicMock, patch

import mongomock
from mongoengine import connect, disconnect

from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.utils.exceptions import (
    ClientNotFound,
    EmailAlreadyRegistered,
    ProductAlreadyRegistered,
    ProductNotFound,
)


class TestClientRepository(unittest.TestCase):
    def setUp(self) -> None:
        disconnect()
        connect(
            "mongoenginetest",
            mongo_client_class=mongomock.MongoClient,
            uuidRepresentation="standard",
        )

    def tearDown(self) -> None:
        disconnect()

    @patch("app.repositories.client_repository.Client.objects")
    def test_create_client_success(self, mock_client_objects):
        mock_client_objects.return_value.first.return_value = None
        mock_client = Client(name="Ana", email="ana.b@example.com")
        mock_client_objects.return_value.create.return_value = mock_client

        client = ClientRepository.create_client(name="Ana", email="ana.b@example.com")

        self.assertEqual(client.name, "Ana")
        self.assertEqual(client.email, "ana.b@example.com")

    @patch("app.repositories.client_repository.Client.objects")
    def test_create_client_email_already_registered(self, mock_client_objects):
        mock_client_objects.return_value.first.return_value = MagicMock()

        with self.assertRaises(EmailAlreadyRegistered):
            ClientRepository.create_client(name="Ana", email="ana.b@example.com")

    @patch("app.repositories.client_repository.Client.objects")
    def test_get_client_by_id_success(self, mock_client_objects):
        mock_client = MagicMock()
        mock_client_objects.return_value.first.return_value = mock_client

        client = ClientRepository.get_client_by_id(client_id="123")

        self.assertEqual(client, mock_client)

    @patch("app.repositories.client_repository.Client.objects")
    def test_get_client_by_id_not_found(self, mock_client_objects):
        mock_client_objects.return_value.first.return_value = None

        client = ClientRepository.get_client_by_id(client_id="123")

        self.assertIsNone(client)

    @patch("app.repositories.client_repository.Client.objects")
    def test_update_client_success(self, mock_client_objects):
        mock_client = MagicMock()
        mock_client_objects.return_value.first.return_value = mock_client

        updated_client = ClientRepository.update_client(
            client_id="123", name="Beatriz", email="beatriz.ela@example.com"
        )

        self.assertEqual(updated_client, mock_client)
        self.assertEqual(mock_client.name, "Beatriz")
        self.assertEqual(mock_client.email, "beatriz.ela@example.com")
        mock_client.save.assert_called_once()

    @patch("app.repositories.client_repository.Client.objects")
    def test_update_client_not_found(self, mock_client_objects):
        mock_client_objects.return_value.first.return_value = None

        with self.assertRaises(ClientNotFound):
            ClientRepository.update_client(
                client_id="123", name="Beatriz", email="beatriz.ela@example.com"
            )

    @patch("app.repositories.client_repository.Client.objects")
    def test_delete_client_success(self, mock_client_objects):
        mock_client = MagicMock()
        mock_client_objects.return_value.first.return_value = mock_client

        response = ClientRepository.delete_client(client_id="123")

        self.assertEqual(response, {"message": "Client deleted"})
        mock_client.delete.assert_called_once()

    @patch("app.repositories.client_repository.Client.objects")
    def test_delete_client_not_found(self, mock_client_objects):
        mock_client_objects.return_value.first.return_value = None

        with self.assertRaises(ClientNotFound):
            ClientRepository.delete_client(client_id="123")

    @patch("app.repositories.client_repository.requests.get")
    @patch("app.repositories.client_repository.Client.objects")
    def test_add_favorite_success(self, mock_client_objects, mock_requests_get):
        mock_client = MagicMock()
        mock_client.favorites = []
        mock_client_objects.return_value.first.return_value = mock_client
        mock_requests_get.return_value.json.return_value = {"id": "product_1"}

        response = ClientRepository.add_favorite(
            client_id="123", product_id="product_1"
        )

        self.assertEqual(response, {"message": "Product added to favorites"})
        self.assertIn("product_1", mock_client.favorites)
        mock_client.save.assert_called_once()

    @patch("app.repositories.client_repository.requests.get")
    @patch("app.repositories.client_repository.Client.objects")
    def test_add_favorite_already_registered(
        self, mock_client_objects, mock_requests_get
    ):
        mock_client = MagicMock()
        mock_client.favorites = ["product_1"]
        mock_client_objects.return_value.first.return_value = mock_client

        with self.assertRaises(ProductAlreadyRegistered):
            ClientRepository.add_favorite(client_id="123", product_id="product_1")

    @patch("app.repositories.client_repository.Client.objects")
    def test_list_favorites_success(self, mock_client_objects):
        mock_client = MagicMock()
        mock_client.favorites = ["product_1", "product_2"]
        mock_client_objects.return_value.first.return_value = mock_client

        with patch(
            "app.repositories.client_repository.requests.get"
        ) as mock_requests_get:
            mock_requests_get.side_effect = [
                MagicMock(
                    json=MagicMock(
                        return_value={"id": "product_1", "name": "TV 55 Polegadas"}
                    )
                ),
                MagicMock(
                    json=MagicMock(
                        return_value={"id": "product_2", "name": "Air Fryer Electrolux"}
                    )
                ),
            ]

            favorites = ClientRepository.list_favorites(client_id="123")

            self.assertEqual(len(favorites), 2)
            self.assertEqual(favorites[0]["id"], "product_1")
            self.assertEqual(favorites[1]["id"], "product_2")

    @patch("app.repositories.client_repository.Client.objects")
    def test_delete_favorite_success(self, mock_client_objects):
        mock_client = MagicMock()
        mock_client.favorites = ["product_1"]
        mock_client_objects.return_value.first.return_value = mock_client

        response = ClientRepository.delete_favorite(
            client_id="123", product_id="product_1"
        )

        self.assertEqual(response, {"message": "Product removed from favorites"})
        self.assertNotIn("product_1", mock_client.favorites)
        mock_client.save.assert_called_once()

    @patch("app.repositories.client_repository.Client.objects")
    def test_delete_favorite_not_found(self, mock_client_objects):
        mock_client = MagicMock()
        mock_client.favorites = []
        mock_client_objects.return_value.first.return_value = mock_client

        with self.assertRaises(ProductNotFound):
            ClientRepository.delete_favorite(client_id="123", product_id="product_1")


if __name__ == "__main__":
    unittest.main()
