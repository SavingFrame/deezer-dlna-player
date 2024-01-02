import asyncio
from typing import Set

from async_upnp_client.aiohttp import AiohttpRequester
from async_upnp_client.client import UpnpDevice
from async_upnp_client.client_factory import UpnpFactory
from async_upnp_client.const import SsdpSource
from async_upnp_client.ssdp_listener import SsdpListener, SsdpDevice

from dlna.api.v1.schemas.dlna_device import DlnaDeviceSchema
from dlna.utils import send_message_to_clients


class DlnaDevicesManager:
    def __init__(self):
        self.devices: Set[UpnpDevice] = set()

    async def callback(self, ssdp_device: SsdpDevice, device_or_service_type: str, ssdp_source: SsdpSource):
        if not device_or_service_type == 'urn:schemas-upnp-org:device:MediaRenderer:1':
            return
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)
        device = await factory.async_create_device(ssdp_device.location)
        print(device.device_info)
        self.devices.add(device)

    async def discover_devices(self):
        listener = SsdpListener(async_callback=self.callback)
        await listener.async_start()
        await listener.async_search()

    async def update_devices(self):
        message = [
            DlnaDeviceSchema.model_validate(device.device_info).model_dump()
            for device in self.devices
        ]
        print('send message', message)
        await send_message_to_clients(message, 'devices')

    async def periodical_update_devices(self):
        while True:
            await self.update_devices()
            await asyncio.sleep(15)


dlna_manager = DlnaDevicesManager()
