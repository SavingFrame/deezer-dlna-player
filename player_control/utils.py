import logging
from functools import wraps
from typing import Callable

from async_upnp_client.aiohttp import AiohttpRequester
from async_upnp_client.client_factory import UpnpFactory

from dlna.services.dlna_device import DlnaDevice

logger = logging.getLogger('task_worker')


def get_dlna_device(func: Callable):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        data = args[0]
        device = data.get("device")
        if not device:
            logger.error("Device_udh not found in message.")
            raise ValueError("Device_udh not found in message.")
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)
        upnp_device = await factory.async_create_device(device.get("device_url"))
        dlna_device = DlnaDevice(upnp_device, subscribe=False)
        return await func(dlna_device, *args, **kwargs)
    return wrapped

