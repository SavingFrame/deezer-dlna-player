import asyncio
import importlib
import json
import logging
from pathlib import Path

from aio_pika import connect_robust, RobustConnection, Message
from aio_pika.abc import AbstractIncomingMessage, DeliveryMode

from config import settings
from utils.task_worker.task_registry import TASK_REGISTRY

logger = logging.getLogger('task_worker')
logger.setLevel(logging.INFO)
# logging.basicConfig(level=logging.INFO)


class PlayerTaskWorker:

    def __init__(self, connection: RobustConnection | None = None):
        self.connection = connection
        self.channel = None
        self.queue = None
        self.devices = dict()

    async def connect(self):
        self.connection = self.connection or await connect_robust()
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(
            "task_queue",
            durable=True,
        )

    async def run_worker(self):
        await self.connect()
        await self.import_task_modules()
        await self._log_registered_tasks()
        async with self.connection:
            # Creating a channel
            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=1)

            # Declaring queue
            queue = await channel.declare_queue(
                "task_queue",
                durable=True,
            )

            # Start listening the queue with name 'task_queue'
            await queue.consume(self._on_message)

            print(" [*] Waiting for messages. To exit press CTRL+C")
            await asyncio.Future()

    async def on_message(self, data: dict | list) -> None:
        logger.debug("Received message: %s", data)
        message_type = data.get("type")
        await self._log_registered_tasks()
        await TASK_REGISTRY[message_type].task_func(data)

    async def send_message(self, message: dict | list):
        if not self.connection:
            await self.connect()
        message = json.dumps(message)
        message = Message(
            message.encode(), delivery_mode=DeliveryMode.PERSISTENT,
        )
        await self.channel.default_exchange.publish(
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
            await self.on_message(data_json)


if __name__ == "__main__":
    asyncio.run(PlayerTaskWorker().run_worker())
