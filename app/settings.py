import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "segredo_magalu")
    MONGO_URI = os.getenv(
        "MONGO_URI", "mongodb://admin:admin@localhost:27017/?authSource=admin"
    )
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    PROJECT_NAME = "CustomerFavorites"
    PROJECT_DESCRIPTION = "API for customer favorites"
    API_VERSION = "1.0.0"
    DEBUG = False
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

    REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379/0")
    REDIS_EXPIRATION_TIME = os.getenv("REDIS_EXPIRATION_TIME", 60)


settings = Settings()
