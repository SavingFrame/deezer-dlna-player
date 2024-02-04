import json
from uuid import UUID

import aio_pika

from utils.rabbitmq import channel_pool
from ws.ws_manager import ConnectionManager, connection_manager


class RabbitMQService:
    def __init__(self, connection_manager_: ConnectionManager):
        self.connection_manager = connection_manager_
        self.exchange_name = "deezer_dlna_player"  # Custom exchange name

    async def _publish_message(self, message: str, headers: dict = None):
        async with channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.DIRECT
            )
            await exchange.publish(
                aio_pika.Message(body=message.encode(), headers=headers),
                routing_key='websockets',  # Empty for fanout type exchange
            )

    async def broadcast_send(self, message: dict):
        text_message = json.dumps(message)
        headers = {'receivers': 'all'}
        await self._publish_message(text_message, headers=headers)

    async def send_to_device(self, message: dict, websockets_uuid: list[str | UUID]):
        headers = {'receivers': str(websockets_uuid)}
        text_message = json.dumps(message)
        await self._publish_message(text_message, headers=headers)

    async def consume_messages(self):
        async with channel_pool.acquire() as channel:
            # Declaring a temporary queue
            queue = await channel.declare_queue('websockets_old', durable=False)
            exchange = await channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.DIRECT
            )
            # Binding the queue to the non-default exchange
            await queue.bind(exchange)

            # Start consuming messages
            async for message in queue:
                if message.routing_key == 'websockets':
                    await self.on_ws_message(message)
                elif message.routing_key == 'deezer_dlna_player':
                    await self.on_upnp_message(message)

    async def on_ws_message(self, message: aio_pika.IncomingMessage):
        headers = message.headers
        receivers = headers.get('receivers', 'all')
        if receivers == 'all':
            await self.connection_manager.broadcast(message.body.decode())
        else:
            await self.connection_manager.send_to(message.body.decode(), receivers)
        await message.ack()

    async def on_upnp_message(self, message: aio_pika.IncomingMessage):
        pass


# FastAPI application setup remains the same...


rabbitmq_service = RabbitMQService(connection_manager_=connection_manager)
