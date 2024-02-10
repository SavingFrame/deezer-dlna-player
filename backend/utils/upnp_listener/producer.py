import asyncio
import logging
from logging.config import dictConfig

import aio_pika
from aio_pika import DeliveryMode

import config
from utils.rabbitmq import channel_pool
from utils.upnp_listener.producer_callback import UpnpListenerProducerCallback

logger = logging.getLogger("upnp_listener.producer")


class UpnpListener:
    async def on_startup(self):
        from dlna.services.dlna_discovery import upnp_devices_discovery

        await upnp_devices_discovery.discover_devices()

    async def run_worker(self):
        await self.on_startup()
        logger.info("UpnpListener started")

    async def send_message(self, message: bytes, headers: dict | None = None):
        async with channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange("deezer_dlna_player", aio_pika.ExchangeType.DIRECT)
            message = aio_pika.Message(
                message,
                headers=headers,
                delivery_mode=DeliveryMode.NOT_PERSISTENT,
            )
            await exchange.publish(
                message,
                routing_key="upnp_listener",
            )


listener = UpnpListener()


async def main():
    await listener.run_worker()
    await UpnpListenerProducerCallback().start_listener()


if __name__ == "__main__":
    dictConfig(config.log_config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
