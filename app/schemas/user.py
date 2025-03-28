from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    password: str
