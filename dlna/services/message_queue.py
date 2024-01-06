import aio_pika

from config import settings
from dlna.services.ws_manager import ConnectionManager, connection_manager


class RabbitMQService:
    def __init__(self, connection_manager_: ConnectionManager):
        self.connection_manager = connection_manager_
        self.connection = None
        self.channel = None
        self.exchange_name = "websocket_exchange"  # Custom exchange name
        self.exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()

        # Declare a non-default exchange
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name, aio_pika.ExchangeType.FANOUT
        )

    async def publish_message(self, message: str):
        await self.exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=''  # Empty for fanout type exchange
        )

    async def consume_messages(self):
        async with self.channel:
            # Declaring a temporary queue
            queue = await self.channel.declare_queue('', durable=True, exclusive=True)

            # Binding the queue to the non-default exchange
            await queue.bind(self.exchange)

            # Start consuming messages
            async for message in queue:
                await self.connection_manager.broadcast(message.body.decode())
                await message.ack()  # Acknowledge the message


# FastAPI application setup remains the same...


rabbitmq_service = RabbitMQService(connection_manager_=connection_manager)
