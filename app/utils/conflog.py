import logging

from pydantic import BaseModel

from app.settings import settings


class ConfLog(BaseModel):
    LOGGER_NAME: str = "customer-favorites-logger"
    LOG_FORMAT: str = (
        "%(levelprefix)s %(asctime)s| %(module)s line %(lineno)d | %(message)s"
    )
    LOG_LEVEL: str = settings.LOG_LEVEL

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


logger = logging.getLogger(ConfLog().LOGGER_NAME)
