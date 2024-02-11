from utils.redis import async_redis


async def clear_subscribers():
    devices = await async_redis.keys("subscribers:*")
    for device in devices:
        await async_redis.delete(device)
