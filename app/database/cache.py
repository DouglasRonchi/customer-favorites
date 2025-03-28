from typing import Optional

import redis

from app.settings import settings
from app.utils.conflog import logger
from app.utils.singleton import SingletonMeta


class RedisClient(metaclass=SingletonMeta):
    def connect(self, host=None):
        self.client = None
        self.redis_uri = host or settings.REDIS_URI
        self.expiration_time = settings.REDIS_EXPIRATION_TIME
        self.client = redis.StrictRedis.from_url(self.redis_uri)

    def set(self, key: str, value: str) -> bool:
        try:
            return self.client.set(name=key, value=value, ex=self.expiration_time)
        except redis.RedisError as e:
            logger.error(f"Error setting value: {e}")
            return False

    def get(self, key: str) -> Optional[str]:
        try:
            return self.client.get(key)
        except redis.RedisError as e:
            logger.error(f"Error getting value: {e}")
            return None

    def close(self):
        try:
            self.client.close()
            logger.info("Connection to Redis closed.")
        except redis.RedisError as e:
            logger.error(f"Error closing connection: {e}")
