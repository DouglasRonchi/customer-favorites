from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from jose import jwt

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserBase
from app.settings import Settings
from app.utils.conflog import logger
from app.utils.exceptions import UserEmailAlreadyRegistered

router = APIRouter(tags=["Auth"])
settings = Settings()
user_repository = UserRepository()


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
):
    logger.info("Creating access token")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


@router.post("/login")
async def login(user_create: UserBase):
    logger.info("Login request received")
    try:
        user = user_repository.get_user_by_email(user_create.email)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


@router.post("/register")
async def register_user(user_create: UserBase):
    logger.info("Register request received")
    try:
        existing_user = user_repository.get_user_by_email(user_create.email)
        if existing_user is not None:
            raise UserEmailAlreadyRegistered

        user = user_repository.create_user(
            email=user_create.email,
            name=user_create.name,
            password=user_create.password,
        )

        access_token = create_access_token(data={"sub": user.email})

        return {
            "Message": "User created with success!",
            "access_token": access_token,
            "token_type": "bearer",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
