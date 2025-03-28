import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.models.user import User
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientBase
from app.schemas.product import Product
from app.utils.conflog import logger

router = APIRouter(tags=["Client"])


@router.post("/clients/", response_model=ClientBase)
def create_client(
    name: str, email: str, current_user: User = Depends(get_current_user)
):
    logger.info(
        f"User {current_user.email} is creating client {name} with email {email}"
    )
    try:
        client = ClientRepository.create_client(name, email)
        return client
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/clients/{client_id}", response_model=ClientBase)
def get_client(client_id: str, current_user: User = Depends(get_current_user)):
    verify_cache_data = ClientRepository.get_cache_data(f"get_client{client_id}")
    if verify_cache_data:
        return json.loads(verify_cache_data)
    logger.info(f"User {current_user.email} is getting client {client_id}")
    client = ClientRepository.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    ClientRepository.set_cache_data(f"get_client{client_id}", str(client.to_json()))
    return client


@router.put("/clients/{client_id}", response_model=ClientBase)
def update_client(
    client_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    logger.info(f"User {current_user.email} is updating client {client_id}")
    try:
        client = ClientRepository.update_client(client_id, name, email)
        return client
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/clients/{client_id}", response_model=dict)
def delete_client(client_id: str, current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.email} is deleting client {client_id}")
    try:
        result = ClientRepository.delete_client(client_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/clients/{client_id}/favorites/")
def add_favorite(
    client_id: str, product_id: str, current_user: User = Depends(get_current_user)
):
    logger.info(
        f"User {current_user.email} is adding product {product_id} to favorites of client {client_id}"
    )
    try:
        result = ClientRepository.add_favorite(client_id, product_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/clients/{client_id}/favorites/", response_model=List[Product])
def list_favorites(client_id: str, current_user: User = Depends(get_current_user)):
    logger.info(
        f"User {current_user.email} is listing favorites for client {client_id}"
    )
    try:
        verify_cache_data = ClientRepository.get_cache_data(
            f"list_favorites{client_id}"
        )
        if verify_cache_data:
            return json.loads(verify_cache_data)
        favorites = ClientRepository.list_favorites(client_id)
        ClientRepository.set_cache_data(
            f"list_favorites{client_id}", json.dumps(favorites)
        )
        return favorites
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/clients/{client_id}/favorites/{product_id}", response_model=dict)
def delete_favorite(
    client_id: str, product_id: str, current_user: User = Depends(get_current_user)
):
    logger.info(
        f"User {current_user.email} is deleting product {product_id} from favorites of client {client_id}"
    )
    try:
        result = ClientRepository.delete_favorite(client_id, product_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
