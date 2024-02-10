import logging
from functools import wraps
from typing import Callable

from async_upnp_client.aiohttp import AiohttpRequester
from async_upnp_client.client_factory import UpnpFactory

from dlna.services.dlna_device import DlnaDevice

logger = logging.getLogger('task_worker')

cache = {}


def get_dlna_device(func: Callable):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        data = kwargs.get('data') or args[0]
        device = data.get("device")
        if not device:
            logger.error("Device not found in message.")
            raise ValueError("Device not found in message.")
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)
        device_udh = device.get('device_udn')
        existing_device = cache.get(device_udh)
        if existing_device:
            return await func(existing_device, *args, **kwargs)
        upnp_device = await factory.async_create_device(device.get("device_url"))
        dlna_device = DlnaDevice(upnp_device, subscribe=False)
        cache[device_udh] = dlna_device
        return await func(dlna_device, *args, **kwargs)

    return wrapped
