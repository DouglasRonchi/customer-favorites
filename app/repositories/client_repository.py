from typing import Any, List, Optional

import requests

from app.database.cache import RedisClient
from app.models.client import Client
from app.schemas.product import Product
from app.utils.conflog import logger
from app.utils.exceptions import (
    ClientNotFound,
    EmailAlreadyRegistered,
    ProductAlreadyRegistered,
    ProductNotFound,
)


class ClientRepository:
    @staticmethod
    def create_client(name: str, email: str) -> Client:
        logger.info("Creating client")
        existing_client = Client.objects(email=email).first()
        if existing_client:
            raise EmailAlreadyRegistered(email=email)

        client = Client(name=name, email=email, favorites=[])
        client.save()
        logger.info("Client created")
        return client

    @staticmethod
    def get_client_by_id(client_id: str) -> Optional[Client]:
        logger.info("Getting client by id")
        return Client.objects(id=client_id).first()

    @staticmethod
    def update_client(
        client_id: str, name: Optional[str] = None, email: Optional[str] = None
    ) -> Client:
        logger.info("Updating client")
        client = Client.objects(id=client_id).first()
        if not client:
            raise ClientNotFound(client_id=client_id)

        if name:
            client.name = name
        if email:
            client.email = email

        client.save()
        logger.info("Client updated")
        return client

    @staticmethod
    def delete_client(client_id: str) -> dict:
        logger.info("Deleting client")
        client = Client.objects(id=client_id).first()
        if not client:
            raise ClientNotFound(client_id=client_id)

        client.delete()
        logger.info("Client deleted")
        return {"message": "Client deleted"}

    @staticmethod
    def add_favorite(client_id: str, product_id: str) -> dict:
        logger.info("Adding favorite product to client list")
        client = Client.objects(id=client_id).first()
        if not client:
            raise ClientNotFound(client_id=client_id)

        for favorite in client.favorites:
            if favorite == product_id:
                raise ProductAlreadyRegistered(product_id=product_id)

        response = requests.get(
            f"http://127.0.0.1:8000/api/product/{product_id}/", timeout=5
        )

        client.favorites.append(response.json().get("id"))
        client.save()
        logger.info("Favorite product added to client list")
        return {"message": "Product added to favorites"}

    @staticmethod
    def list_favorites(client_id: str) -> List[Product]:
        logger.info("Listing favorite products")
        client = Client.objects(id=client_id).first()
        if not client:
            raise ClientNotFound(client_id=client_id)

        favorites = []
        for favorite in client.favorites:
            response = requests.get(
                f"http://127.0.0.1:8000/api/product/{favorite}/", timeout=5
            )
            favorites.append(response.json())
        return favorites

    @staticmethod
    def delete_favorite(client_id: str, product_id: str) -> dict:
        logger.info("Removing favorite product from client list")
        client = Client.objects(id=client_id).first()
        if not client:
            raise ClientNotFound(client_id=client_id)

        product_found = None
        for product in client.favorites:
            if product == product_id:
                product_found = product_id
                break
        if product_found is None:
            raise ProductNotFound(product_id=product_id)

        client.favorites.remove(product_found)
        client.save()
        logger.info("Favorite product removed from client list")
        return {"message": "Product removed from favorites"}

    @staticmethod
    def set_cache_data(key: str, value: Any):
        logger.info("Setting cache data")
        redis = RedisClient()
        redis.set(key, str(value))

    @staticmethod
    def get_cache_data(key: str) -> Any:
        logger.info("Getting cache data")
        redis = RedisClient()
        return redis.get(key)
