from pydantic import BaseModel


class Product(BaseModel):
    price: float
    image: str
    brand: str
    id: str
    title: str
    reviewScore: float
