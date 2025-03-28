from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.cache import RedisClient
from app.database.database import MongoDBConnection
from app.routes import auth, client, mock_products
from app.settings import settings
from app.utils.conflog import ConfLog, logger

dictConfig(ConfLog().model_dump())


def get_application() -> FastAPI:
    logger.info("Creating FastAPI application...")
    MongoDBConnection()
    RedisClient().connect()
    fast_api_app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.API_VERSION,
        debug=settings.DEBUG,
    )

    # Add middleware cors
    origins = ["*"]
    fast_api_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add Routers
    fast_api_app.include_router(client.router)
    fast_api_app.include_router(auth.router)
    fast_api_app.include_router(mock_products.router)

    return fast_api_app


app = get_application()
