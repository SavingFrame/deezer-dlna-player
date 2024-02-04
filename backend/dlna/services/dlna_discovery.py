import asyncio
import logging
import uuid

from async_upnp_client.aiohttp import AiohttpRequester
from async_upnp_client.client import UpnpDevice
from async_upnp_client.client_factory import UpnpFactory
from async_upnp_client.exceptions import UpnpConnectionTimeoutError
from async_upnp_client.ssdp_listener import SsdpListener, SsdpDevice

from dlna.schemas import DlnaDeviceSchema
from dlna.services.dlna_device import DlnaDevice
from utils.broadcaster.utils import send_message_to_clients, send_message_to_specific_clients

logger = logging.getLogger(__name__)


class UpnpDeviceDiscoveryManager:
    def __init__(self):
        self.devices: dict[str, UpnpDevice] = dict()

    async def create_device(self, location_url: str):
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)
        try:
            device = await factory.async_create_device(location_url)
        except UpnpConnectionTimeoutError:
            logger.warning(f"Device timeout {location_url}")
            return
        self.devices[device.udn] = device
        return device

    async def callback(self, ssdp_device: SsdpDevice, device_or_service_type: str, *args, **kwargs):
        if not device_or_service_type == 'urn:schemas-upnp-org:device:MediaRenderer:1':
            return
        logger.info(f"Device founded {ssdp_device.udn} {ssdp_device.location}")
        device = await self.create_device(ssdp_device.location)
        await self.setup_listener(device)
        await self.update_devices()

    async def discover_devices(self):
        listener = SsdpListener(async_callback=self.callback)
        await listener.async_start()
        await listener.async_search()

    async def update_devices(self):
        message = [
            DlnaDeviceSchema.model_validate(device.device_info).model_dump()
            for device in self.devices.values()
        ]
        await send_message_to_clients(message, 'devices')

    async def update_device_for_client(self, client_uuid: str | uuid.UUID):
        message = [
            DlnaDeviceSchema.model_validate(device.device_info).model_dump()
            for device in self.devices.values()
        ]
        await send_message_to_specific_clients(message, 'devices', [client_uuid])

    async def periodical_update_devices(self):
        while True:
            await self.update_devices()
            await asyncio.sleep(15)

    async def setup_listener(self, upnp_device: UpnpDevice):
        DlnaDevice(upnp_device)

    async def add_device_from_listener(self, device_udn: str, device_location: str):
        device = self.devices.get(device_udn)
        if device:
            return
        device = await self.create_device(device_location)
        return device


upnp_devices_discovery = UpnpDeviceDiscoveryManager()
