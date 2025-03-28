from typing import List

from pydantic import BaseModel


class ClientBase(BaseModel):
    email: str
    name: str
    favorites: List[str]
