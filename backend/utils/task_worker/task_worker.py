import asyncio
import importlib
import json
import logging
from pathlib import Path

import aio_pika
from aio_pika.abc import AbstractIncomingMessage, DeliveryMode

from config import settings
from utils.rabbitmq import channel_pool
from utils.task_worker.task_registry import TASK_REGISTRY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('task_worker')
logger.setLevel(logging.INFO)


class PlayerTaskWorker:

    async def run_worker(self):
        await self.import_task_modules()
        await self._log_registered_tasks()
        async with channel_pool.acquire() as channel:
            await channel.set_qos(prefetch_count=1)

            # Declaring queue
            queue = await channel.declare_queue(
                durable=False,
            )
            exchange = await channel.declare_exchange(
                'task_worker', aio_pika.ExchangeType.DIRECT
            )

            await queue.bind(exchange, routing_key="task_queue")
            await queue.bind(exchange, routing_key="upnp_notify")

            # Start listening the queue with name 'task_queue'
            await queue.consume(self._on_message)

            print(" [*] Waiting for messages. To exit press CTRL+C")
            await asyncio.Future()

    async def on_message(self, data: dict | list) -> None:
        logger.debug("Received message: %s", data)
        message_type = data.get("type")
        await TASK_REGISTRY[message_type].task_func(data)

    async def send_message(self, message: dict | list):
        async with channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                'task_worker', aio_pika.ExchangeType.DIRECT
            )
            message = json.dumps(message)
            message = aio_pika.Message(
                message.encode(), delivery_mode=DeliveryMode.NOT_PERSISTENT,
            )
            await exchange.publish(
                message,
                routing_key="task_queue",
            )

    @staticmethod
    async def _find_task_modules():
        task_modules = []
        base_dir_path = Path(settings.BASE_DIR)
        for path in base_dir_path.rglob('tasks*.py'):
            # Convert file path to module path
            relative_path = path.relative_to(base_dir_path)
            module_path = '.'.join(relative_path.with_suffix('').parts)
            task_modules.append(module_path)
        return task_modules

    async def import_task_modules(self):
        task_modules = await self._find_task_modules()
        for module_path in task_modules:
            importlib.import_module(module_path)

    async def _log_registered_tasks(self):
        logger.info("Registered tasks:")
        for task_name, task_instance in TASK_REGISTRY.items():
            logger.info(f"\t[{task_name}] - {task_instance.task_module}")

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            data = message.body.decode()
            data_json = json.loads(data)
            if message.routing_key == 'task_queue':
                await self.on_message(data_json)
            # elif message.routing_key == 'upnp_notify':
            #     await self.upnp_notify_on_message(data_json)

    # async def upnp_notify_on_message(self, data: list | dict) -> None:
    #     logger.info("Received UpnP notify message: %s", data)


if __name__ == "__main__":
    asyncio.run(PlayerTaskWorker().run_worker())
