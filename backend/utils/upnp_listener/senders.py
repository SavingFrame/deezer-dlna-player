import json
import logging

from utils.upnp_listener.producer import listener
from utils.upnp_listener.producer_callback import UpnpListenerProducerCallback

logger = logging.getLogger("upnp_listener.producer")


async def send_message_upnp_listener(message: dict | list, headers: dict | None = None):
    logger.debug(f"Send message to upnp_listener: {message}")
    message = json.dumps(message).encode()
    await listener.send_message(message, headers=headers)


async def send_message_upnp_producer(message: dict | list, headers: dict | None = None):
    logger.debug(f"Send message to upnp_producer callback: {message}")
    message = json.dumps(message).encode()
    await UpnpListenerProducerCallback().send_message(message, headers=headers)
