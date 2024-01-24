import redis
from redis import asyncio as aioredis
from config import settings

async_redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
sync_redis = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
