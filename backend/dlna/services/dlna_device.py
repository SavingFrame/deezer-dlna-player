import asyncio
import logging
import uuid
from datetime import datetime
from typing import Optional

from async_upnp_client.aiohttp import AiohttpNotifyServer
from async_upnp_client.client import UpnpDevice, UpnpStateVariable
from async_upnp_client.profiles.dlna import TransportState
from async_upnp_client.utils import get_local_ip

from dlna.dataclasses import PlaySongInfo
from library.player_queue import TracksQueue
from utils.redis import async_redis
from utils.upnp.dlna import CustomDmrDevice
from utils.upnp_listener.senders import send_message_upnp_listener
from ws.utils import send_message_to_specific_clients

logger = logging.getLogger('dlna_device')


class DlnaDevice:
    def __init__(self, upnp_device: UpnpDevice, subscribe=True):
        self.upnp_device = upnp_device
        self.dmr_device = self.create_dmr_service(upnp_device, subscribe=subscribe)
        self._ws_cache = {}
        self._cached_player_queue: tuple[Optional[TracksQueue], Optional[datetime]] = (None, None)

    async def get_player_queue(self) -> TracksQueue:
        if self._cached_player_queue[1] and (datetime.now() - self._cached_player_queue[1]).seconds < 60:
            return self._cached_player_queue[0]
        player_queue = await TracksQueue.load_from_redis(device=self) or TracksQueue(device=self)
        self._cached_player_queue = (player_queue, datetime.now())
        return player_queue

    async def _set_next_track(self):
        from utils.task_worker.task_worker import PlayerTaskWorker
        logger.info(f"Setting next track on {self.upnp_device.friendly_name}")
        message = {
            'type': 'internal.set_next_track',
            'message': {'next_track_uri': self.dmr_device.next_transport_uri},
            'device': {
                'device_udh': self.upnp_device.udn,
                'device_url': self.upnp_device.device_url,
            }
        }
        await PlayerTaskWorker().send_message(message)

    async def notify_subscribers(self):
        subscribers: set[str] = await async_redis.smembers(f'subscribers:{self.upnp_device.udn}')
        send_to = []
        if not subscribers:
            return
        message = self.player_info()
        for ws_uuid in subscribers:
            cached_message = self._ws_cache.get(ws_uuid)
            if cached_message == message:
                continue
            self._ws_cache[ws_uuid] = message
            send_to.append(ws_uuid)
        await send_message_to_specific_clients(type='player', message=message, websockets_uuid=send_to)

    async def subscribe(self, ws_uuid: str):
        await async_redis.sadd(f'subscribers:{self.upnp_device.udn}', ws_uuid)

    async def notify_specific_subscribers(self, websockets_uuid: list[str, uuid.UUID]):
        message = self.player_info()
        websockets_uuid = [str(ws_uuid) for ws_uuid in websockets_uuid]
        await send_message_to_specific_clients(type='player', message=message, websockets_uuid=websockets_uuid)

    async def start_listener(self, server: AiohttpNotifyServer, device: CustomDmrDevice):
        await server.async_start_server()
        await device.async_subscribe_services(auto_resubscribe=True)

    async def play_song(self, song_info: PlaySongInfo):
        await self.dmr_device.async_set_transport_uri(
            media_url=song_info.media_url,
            media_title='',
            meta_data=song_info.metadata
        )
        await self.dmr_device.async_play()
        logger.info(f"Playing {song_info.media_url} on {self.upnp_device.friendly_name}")

    async def set_next_song(self, song_info: PlaySongInfo):
        await self.dmr_device.async_set_next_transport_uri(
            media_url=song_info.media_url,
            media_title='',
            meta_data=song_info.metadata
        )
        logger.info(f"Setting next song {song_info.media_url} on {self.upnp_device.friendly_name}")

    def player_info(self):

        return {
            'media_title': self.dmr_device.media_title,
            'media_artist': self.dmr_device.media_artist,
            'media_position': self.dmr_device.media_position,
            'media_duration': self.dmr_device.media_duration,
            'is_playing': self.is_playing,
            'volume_level': self.dmr_device.volume_level,
            'media_album': self.dmr_device.media_album_name,
            'media_image_url': self.dmr_device.media_image_url,
        }

    @property
    def is_playing(self):
        transport_state = self.dmr_device.transport_state
        if transport_state in [TransportState.PLAYING, TransportState.TRANSITIONING]:
            return True
        return False

    async def pause(self):
        logger.info(f"Pausing {self.upnp_device.friendly_name}")
        await self.dmr_device.async_pause()

    async def play(self):
        logger.info(f"Playing {self.upnp_device.friendly_name}")
        await self.dmr_device.async_play()

    async def set_volume(self, volume: int | float):
        if 1 < volume < 100:
            volume = volume / 100
        elif volume > 100:
            volume = 0.10
        logger.info(f"Setting volume {volume} to {self.upnp_device.friendly_name}")
        await self.dmr_device.async_set_volume_level(volume)

    async def _send_event_to_queue(self, service, state_variables: list[UpnpStateVariable]):
        data = {
            'service_id': service.service_id,
            'state_variables': [{'name': state_variable.name, 'upnp_value': state_variable.upnp_value}
                                for state_variable in state_variables]
        }
        message = {
            'message': data,
            'device': {'device_udh': self.upnp_device.udn, 'device_url': self.upnp_device.device_url}
        }
        await send_message_upnp_listener(message)

    async def _on_queue_event(self, service, state_variables):
    #     asyncio.create_task(self.on_queue_event(service, state_variables))
        await self.on_queue_event(service, state_variables)

    async def on_queue_event(self, service, state_variables):
        await self.notify_subscribers()
        for var in state_variables:
            if var.name == 'AVTransportURI':
                player_queue = await self.get_player_queue()
                new_track_uri = var.value
                current_track_uri = await player_queue.get_current_track_uri()
                if new_track_uri != current_track_uri:
                    await player_queue.update_current_track_uri(new_track_uri)
                    await self._set_next_track()

    def create_dmr_service(self, upnp_device: UpnpDevice, subscribe=True, subscribe_to_queue=True):

        if not subscribe:
            dmr_device = CustomDmrDevice(self.upnp_device, None)
            dmr_device.on_queue_event = self._on_queue_event if subscribe_to_queue else None
            return dmr_device
        source = (get_local_ip(upnp_device.device_url), 0)
        server = AiohttpNotifyServer(upnp_device.requester, source=source)
        dmr_device = CustomDmrDevice(self.upnp_device, server.event_handler)
        dmr_device.on_event = self._on_event
        dmr_device.on_queue_event = self._on_queue_event if subscribe_to_queue else None
        asyncio.create_task(self.start_listener(server, dmr_device))
        return dmr_device

    @staticmethod
    async def unsubscribe_all(ws_uuid: str):
        devices = await async_redis.keys('subscribers:*')
        for device in devices:
            await async_redis.srem(device, ws_uuid)

    def _on_event(self, service, state_variables):
        asyncio.create_task(self._send_event_to_queue(service, state_variables))
