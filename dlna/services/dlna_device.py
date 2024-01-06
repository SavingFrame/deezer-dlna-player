import asyncio
import dataclasses
import logging
import posixpath
import urllib.parse

from async_upnp_client.aiohttp import AiohttpNotifyServer
from async_upnp_client.client import UpnpDevice
from async_upnp_client.profiles.dlna import DmrDevice
from async_upnp_client.utils import get_local_ip

from config import settings
from dlna.utils import send_message_to_clients

logger = logging.getLogger('dlna_device')


@dataclasses.dataclass
class DlnaSongMetadata:
    artist: str
    album: str
    title: str


class DlnaDevice:
    def __init__(self, upnp_device: UpnpDevice, subscribe=True):
        self.upnp_device = upnp_device
        self.dmr_device = self.create_dmr_service(upnp_device, subscribe=subscribe)

    def on_event(self, *args, **kwargs):
        print('on event')
        message = self.player_info()
        asyncio.create_task(send_message_to_clients(type='player', message=message))

    def create_dmr_service(self, upnp_device: UpnpDevice, subscribe=True):
        if not subscribe:
            return DmrDevice(self.upnp_device, None)
        source = (get_local_ip(upnp_device.device_url), 0)
        server = AiohttpNotifyServer(upnp_device.requester, source=source)
        asyncio.create_task(server.async_start_server())
        dmr_device = DmrDevice(self.upnp_device, server.event_handler)
        asyncio.create_task(dmr_device.async_subscribe_services(auto_resubscribe=True))
        dmr_device.on_event = self.on_event
        return dmr_device

    async def play_song(self, file_path: str, metadata: DlnaSongMetadata):
        file_path = file_path.replace(settings.MEDIA_PATH, '', 1)
        if file_path.startswith('/'):
            file_path = file_path[1:]
        url = posixpath.join(settings.MEDIA_URL, urllib.parse.quote(file_path))
        metadata_dict = dataclasses.asdict(metadata)
        await self.get_dmr_device()
        await self.dmr_device.async_set_transport_uri(
            url,
            media_title=metadata.title,
            meta_data=metadata_dict
        )
        await self.dmr_device.async_play()
        logger.info(f"Playing {url} on {self.upnp_device.friendly_name}")

    def player_info(self):
        return {
            'media_title': self.dmr_device.media_title,
            'media_artist': self.dmr_device.media_artist,
            'media_position': self.dmr_device.media_position,
            'media_duration': self.dmr_device.media_duration,
            'has_play_media': self.dmr_device.has_play_media,
            'volume_level': self.dmr_device.volume_level
        }

    async def toggle_play_pause(self):
        await self.get_dmr_device()
        await self.dmr_device.has_play_media()
        logger.info(f"Toggling play/pause on {self.upnp_device.friendly_name}")
