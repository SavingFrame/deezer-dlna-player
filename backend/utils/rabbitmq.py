import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from config import settings


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.RABBITMQ_URL)

connection_pool: Pool = Pool(get_connection, max_size=2)


async def get_channel() -> aio_pika.Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()

channel_pool: Pool = Pool(get_channel, max_size=10)

# rabbit_connection = await aio_pika.connect_robust(
#     url=settings.RABBITMQ_URL
# )
