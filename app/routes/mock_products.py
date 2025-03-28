from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.product import Product
from app.utils.conflog import logger

router = APIRouter(tags=["MockProducts"])

MOCK_PRODUCTS = [
    Product(
        price=59.90,
        image="url/product_1.jpg",
        brand="Brand A",
        id="product_1",
        title="Produto 1",
        reviewScore=4.5,
    ),
    Product(
        price=120,
        image="url/product_2.jpg",
        brand="Brand B",
        id="product_2",
        title="Produto 2",
        reviewScore=3.8,
    ),
    Product(
        price=299.90,
        image="url/product_3.jpg",
        brand="Brand C",
        id="product_3",
        title="Produto 3",
        reviewScore=4.2,
    ),
    Product(
        price=470,
        image="url/product_4.jpg",
        brand="Brand D",
        id="product_4",
        title="Produto 4",
        reviewScore=4.7,
    ),
]


@router.get("/api/product/", response_model=List[Product])
async def list_products(page: int = 1, limit: int = 10):
    logger.info(f"Listing products from page {page} with limit {limit}")
    start_index = (page - 1) * limit
    end_index = start_index + limit
    return MOCK_PRODUCTS[start_index:end_index]


@router.get("/api/product/{product_id}", response_model=Product)
async def get_product_details(product_id: str):
    logger.info(f"Getting details for product {product_id}")
    for product in MOCK_PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=400, detail=str("Product not found"))
