import fakeredis
import pytest


@pytest.fixture
def redis_client():
    fake_redis = fakeredis.FakeStrictRedis()

    from app.database.cache import RedisClient

    client = RedisClient(redis_uri="redis://localhost:6379")
    client = fake_redis
    client.get = fake_redis.get
    client.set = fake_redis.set

    return client
