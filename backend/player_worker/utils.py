import logging
from functools import wraps
from typing import Callable

from async_upnp_client.aiohttp import AiohttpRequester
from async_upnp_client.client_factory import UpnpFactory
from async_upnp_client.exceptions import UpnpConnectionTimeoutError

from dlna.services.dlna_device import DlnaDevice

logger = logging.getLogger("task_worker")

cache = {}


def get_dlna_device(func: Callable):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        data = kwargs.get("data") or args[0]
        device = data.get("device")
        if not device:
            logger.error("Device not found in message.")
            raise ValueError("Device not found in message.")
        device_udn = device.get("device_udn")
        existing_device = cache.get(device_udn)
        if existing_device:
            return await func(existing_device, *args, **kwargs)
        try:
            requester = AiohttpRequester()
            factory = UpnpFactory(requester)
            upnp_device = await factory.async_create_device(device.get("device_url"))
        except UpnpConnectionTimeoutError as error:
            logger.error(f"Connection error to {device.get('device_url')}")
            raise ValueError(f"Connection error to {device.get('device_url')}") from error
        dlna_device = DlnaDevice(upnp_device, subscribe=False)
        cache[device_udn] = dlna_device
        return await func(dlna_device, *args, **kwargs)

    return wrapped
