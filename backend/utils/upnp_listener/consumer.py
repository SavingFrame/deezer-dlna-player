import asyncio
import json
import logging

import aio_pika
from aio_pika import IncomingMessage

from utils.rabbitmq import channel_pool

logger = logging.getLogger('upnp_listener.consumer')


class UpnpListenerConsumer:

    def __init__(self):
        self._listener_task: asyncio.Task | None = None

    async def start_listener(self):
        self._listener_task = asyncio.create_task(self._listener())
        self._listener_task.add_done_callback(self._task_callback)

    def _task_callback(self, task: asyncio.Task):
        if task.cancelled():
            logger.info("Upnp Listener Consumer task was cancelled")
        elif task.done():
            try:
                task.result()
            except asyncio.CancelledError:
                logger.info("Upnp Listener Consumer task was cancelled")
            except Exception as e:
                logger.exception("Upnp Listener Consumer task failed", exc_info=e)

    async def stop_listener(self):
        if self._listener_task.done():
            self._listener_task.result()
        else:
            self._listener_task.cancel()

    async def on_message(self, message: dict | list, headers: dict):
        if headers.get('type') == 'discovery':
            from dlna.services.dlna_discovery import upnp_devices_discovery
            await upnp_devices_discovery.create_device_from_listener(
                device_udn=message['udn'],
                device_location=message['location']
            )
        else:
            logger.warning(f"Unknown message type: {headers.get('type')} message: {message}")

    async def _listener(self):
        logger.info("Upnp Listener Consumer started")
        async with channel_pool.acquire() as channel:
            # Declaring a temporary queue
            queue = await channel.declare_queue('upnp_listener')
            exchange = await channel.declare_exchange(
                'deezer_dlna_player', aio_pika.ExchangeType.DIRECT
            )
            # Binding the queue to the non-default exchange
            await queue.bind(exchange, routing_key='upnp_listener')

            # Start consuming messages
            message: IncomingMessage
            async for message in queue:
                await self._on_message(message)

    async def _on_message(self, message: IncomingMessage):
        logger.debug(f"Message received: {message.body}, headers: {message.headers}")
        json_message = json.loads(message.body)
        await self.on_message(json_message, message.headers)
        await message.ack()
