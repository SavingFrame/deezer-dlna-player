import logging

from async_upnp_client.aiohttp import AiohttpRequester
from async_upnp_client.client import UpnpDevice
from async_upnp_client.client_factory import UpnpFactory
from async_upnp_client.exceptions import UpnpConnectionError, UpnpConnectionTimeoutError
from async_upnp_client.ssdp_listener import SsdpDevice, SsdpListener

from dlna.schemas import UpnpDeviceSchema
from dlna.services.dlna_device import DlnaDevice
from utils.upnp_listener.senders import send_message_upnp_listener
from ws.utils import send_message_to_clients, send_message_to_specific_clients

logger = logging.getLogger("upnp.discovery")


class UpnpDeviceDiscoveryManager:
    def __init__(self):
        self.devices: dict[str, UpnpDevice] = dict()

    async def _create_device(self, location_url: str):
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)
        try:
            device = await factory.async_create_device(location_url)
        except (UpnpConnectionTimeoutError, UpnpConnectionError) as err:
            logger.warning(f"Connection error to {location_url}: {str(err)}")
            return
        self.devices[device.udn] = device
        logger.info(f"Device created {device.udn} {device.friendly_name}")
        return device

    async def callback(self, ssdp_device: SsdpDevice, device_or_service_type: str, *args, **kwargs):
        if device_or_service_type != "urn:schemas-upnp-org:device:MediaRenderer:1":
            return
        logger.info(f"Device founded {ssdp_device.udn} {ssdp_device.location}")
        device = await self._create_device(ssdp_device.location)
        if not device:
            return
        await self.send_to_listener(ssdp_device.udn, ssdp_device.location)
        await self.setup_listener(device)
        await self.send_devices_to_websockets()

    async def discover_devices(self):
        listener = SsdpListener(async_callback=self.callback)
        await listener.async_start()
        await listener.async_search()

    async def send_devices_to_websockets(self, clients: list[str] = None):
        message = [
            UpnpDeviceSchema.model_validate(device.device_info).model_dump() for device in self.devices.values()
        ]
        if clients:
            await send_message_to_specific_clients(message, "devices", clients)
        else:
            await send_message_to_clients(message, "devices")

    async def setup_listener(self, upnp_device: UpnpDevice):
        DlnaDevice(upnp_device)

    async def send_to_listener(self, udn: str, location: str):
        headers = {
            "type": "discovery",
        }
        message = {
            "udn": udn,
            "location": location,
        }
        await send_message_upnp_listener(message, headers=headers)

    async def send_all_devices_to_listener(self):
        for device in self.devices.values():
            await self.send_to_listener(device.udn, device.device_url)

    async def create_device_from_listener(self, device_udn: str, device_location: str):
        if self.devices.get(device_udn):
            return
        await self._create_device(device_location)


upnp_devices_discovery = UpnpDeviceDiscoveryManager()
