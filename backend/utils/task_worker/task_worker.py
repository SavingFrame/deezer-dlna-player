import asyncio
import importlib
import json
import logging
from logging.config import dictConfig
from pathlib import Path

import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from pyinstrument import Profiler

import config
from config import settings
from utils.rabbitmq import channel_pool
from utils.task_worker.task_registry import TASK_REGISTRY
from utils.upnp_listener.senders import send_message_upnp_producer

logger = logging.getLogger('task_worker')
logger.setLevel(logging.DEBUG)
profiler = Profiler()


class PlayerTaskWorker:

    async def on_setup(self):
        await send_message_upnp_producer({'action': 'devices.get'})

    async def run_worker(self):
        await self.import_task_modules()
        await self._log_registered_tasks()
        async with channel_pool.acquire() as channel:
            # Declaring queue
            queue = await channel.declare_queue(
                "task_worker", durable=False,
            )
            exchange = await channel.declare_exchange(
                'deezer_dlna_player', aio_pika.ExchangeType.DIRECT
            )

            await queue.bind(exchange, routing_key="task_worker")
            await queue.bind(exchange, routing_key="upnp_listener")

            # Start listening the queue with name 'task_queue'
            await queue.consume(self._on_message)
            await self.on_setup()
            print(" [*] Waiting for messages. To exit press CTRL+C")
            await asyncio.Future()

    async def on_message(self, data: dict | list) -> None:
        logger.debug("Received message: %s", data)
        message_type = data.get("type")
        await TASK_REGISTRY[message_type].task_func(data)

    async def send_message(self, message: dict | list):
        async with channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                'deezer_dlna_player', aio_pika.ExchangeType.DIRECT
            )
            logger.debug("Sending message to task worker: %s", message)
            message = json.dumps(message)
            message = aio_pika.Message(
                message.encode(),
            )
            await exchange.publish(
                message,
                routing_key="task_worker",
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

            logger.debug("Message received: %s,  %s", message.body, message.routing_key)
            data = message.body.decode()
            data_json = json.loads(data)
            if message.routing_key == 'task_worker':
                await self.on_message(data_json)
            elif message.routing_key == 'upnp_listener':
                if message.headers.get('type') == 'discovery':
                    from dlna.services.dlna_discovery import upnp_devices_discovery
                    await upnp_devices_discovery.create_device_from_listener(
                        device_udn=data_json['udn'],
                        device_location=data_json['location']
                    )
                else:
                    await TASK_REGISTRY['upnp_listener.event'].task_func(data=data_json)


if __name__ == "__main__":
    dictConfig(config.log_config)
    asyncio.run(PlayerTaskWorker().run_worker())
