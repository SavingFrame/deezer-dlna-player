import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, AsyncIterator, Dict, Optional

import aio_pika

from utils.rabbitmq import channel_pool


class Event:
    def __init__(self, message: str, headers: dict | None = None) -> None:
        self.headers: dict | None = headers or {}
        self.message: str = message

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Event)
            and self.headers == other.headers
            and self.message == other.message
        )

    def __repr__(self) -> str:
        return f"Event(headers={self.headers!r}, message={self.message!r})"


class Unsubscribed(Exception):
    pass


class Broadcast:

    def __init__(self):
        self._subscribers: Dict[str, set[asyncio.Queue]] = {}

    async def __aenter__(self) -> "Broadcast":
        await self.connect()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        self._listener_task = asyncio.create_task(self._listener())

    async def disconnect(self) -> None:
        print('disconnect')
        if self._listener_task.done():
            self._listener_task.result()
        else:
            self._listener_task.cancel()

    async def _listener(self) -> None:
        async with channel_pool.acquire() as channel:
            # Declaring a temporary queue
            queue = await channel.declare_queue('websockets')
            exchange = await channel.declare_exchange(
                'deezer_dlna_player', aio_pika.ExchangeType.DIRECT
            )
            # Binding the queue to the non-default exchange
            await queue.bind(exchange, routing_key='websockets')

            # Start consuming messages
            async for message in queue:
                event = Event(message.body.decode(), headers=message.headers)

                for queue in list(self._subscribers.get('websockets', [])):
                    await queue.put(event)
                await message.ack()

    async def publish(self, message: Any, headers=None) -> None:
        async with channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                'deezer_dlna_player', aio_pika.ExchangeType.DIRECT
            )
            await exchange.publish(
                aio_pika.Message(body=message.encode(), headers=headers),
                routing_key='websockets',  # Empty for fanout type exchange
            )

    @asynccontextmanager
    async def subscribe(self) -> AsyncIterator["Subscriber"]:
        queue: asyncio.Queue = asyncio.Queue()
        channel = "websockets"
        try:
            if not self._subscribers.get(channel):
                self._subscribers[channel] = {queue}
            else:
                self._subscribers[channel].add(queue)

            yield Subscriber(queue)

            self._subscribers[channel].remove(queue)
            if not self._subscribers.get(channel):
                del self._subscribers[channel]
        finally:
            await queue.put(None)


class Subscriber:
    def __init__(self, queue: asyncio.Queue) -> None:
        self._queue = queue

    async def __aiter__(self) -> Optional[AsyncGenerator]:
        try:
            while True:
                yield await self.get()
        except Unsubscribed:
            pass

    async def get(self) -> Event:
        while True:
            try:
                item = self._queue.get_nowait()
                if item is None:
                    raise Unsubscribed()
                return item
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.5)
