import json
import logging
import random
from typing import TYPE_CHECKING, Optional

from deezer import DeezerError

from deezer_integration.exceptions import NonStreamable
from library.track import Track
from utils import redis

if TYPE_CHECKING:
    from dlna.services.dlna_device import DlnaDevice

logger = logging.getLogger("player_queue")


class TracksQueue:
    def __init__(self, device: "DlnaDevice", tracks: list["Track"] = None):
        self.device = device
        self.tracks = tracks or []
        self.all_tracks = tracks or []
        self.current_track: Optional["Track"] = None
        self.next_track: Optional["Track"] = None
        self.is_shuffle = False

    async def set_queue(self, tracks: list["Track"], start_from: int = None):
        self.all_tracks = tracks
        if start_from:
            tracks = self.move_queue_tracks(tracks, start_from)
        self.tracks = tracks
        await self.save_to_redis()

    async def update_current_track_uri(self, current_track_uri: str):
        await redis.async_redis.set(f"current_track_uri:{self.device.upnp_device.udn}", current_track_uri)
        await self.save_to_redis()

    async def get_current_track_uri(self):
        current_track_uri = await redis.async_redis.get(f"current_track_uri:{self.device.upnp_device.udn}")
        return current_track_uri

    async def set_next_song(self, skip_shuffle: bool = False):
        if not self.tracks:
            logger.info("No tracks in queue")
            return
        if self.is_shuffle and not skip_shuffle:
            track = random.choice(self.tracks)
            self.tracks.remove(track)
        else:
            track = self.tracks.pop(0)
        try:
            play_song_info = await track.generate_play_song_info(download=True)
        except (DeezerError, NonStreamable) as error:
            logger.error(f"Error while getting song info: {error}")
            return await self.set_next_song(skip_shuffle=skip_shuffle)
        self.next_track = track
        await self.device.set_next_song(play_song_info)
        await self.save_to_redis()

    async def toggle_shuffle(self):
        self.is_shuffle = not self.is_shuffle
        await self.set_next_song()
        await self.save_to_redis()

    async def add_next_song(self, track: "Track"):
        if self.tracks[0] != track:
            self.tracks.insert(0, track)
        await self.set_next_song()

    async def play(self):
        if not self.tracks:
            return
        track = self.tracks.pop(0)
        self.current_track = track
        await track.play()
        # if self.tracks:
        #     await self.set_next_song()
        await self.save_to_redis()

    async def play_next(self):
        if not self.tracks:
            return
        self.current_track = self.next_track
        track = self.current_track
        await track.play()
        await self.save_to_redis()

    @property
    def current_track_index(self) -> int | None:
        for index, track in enumerate(self.all_tracks):
            if track.id == self.current_track.id:
                return index
        return None

    async def play_previous(self):
        current_track_index = self.current_track_index
        track_to_play = self.all_tracks[current_track_index - 1] if current_track_index else None
        if not track_to_play:
            return
        self.tracks.insert(0, track_to_play)
        self.current_track = track_to_play
        self.next_track = self.all_tracks[current_track_index]
        await track_to_play.play()
        await self.save_to_redis()

    def move_queue_tracks(self, tracks: list["Track"], start_from_track_id: int):
        for index, track in enumerate(tracks):
            if track.id == start_from_track_id:
                tracks = tracks[index:] + tracks[:index]
                break
        return tracks

    async def save_to_redis(self):
        json_str = json.dumps(self.to_dict())
        await redis.async_redis.set(f"queue:{self.device.upnp_device.udn}", json_str)

    def sync_save_to_redis(self):
        json_str = json.dumps(self.to_dict())
        redis.sync_redis.set(f"queue:{self.device.upnp_device.udn}", json_str)

    @classmethod
    async def load_from_redis(cls, device: "DlnaDevice"):
        json_str = await redis.async_redis.get(f"queue:{device.upnp_device.udn}")
        if not json_str:
            return None
        data = json.loads(json_str)
        return cls.from_dict(device, data)

    def to_dict(self):
        return {
            "tracks": [track.to_dict() for track in self.tracks],
            "current_track": self.current_track.to_dict() if self.current_track else None,
            "next_track": self.next_track.to_dict() if self.next_track else None,
            "all_tracks": [track.to_dict() for track in self.all_tracks],
            "is_shuffle": self.is_shuffle,
        }

    @classmethod
    def from_dict(cls, device: "DlnaDevice", data: dict):
        tracks = [Track.from_dict(track_data, dlna_device=device) for track_data in data["tracks"]]
        current_track = Track.from_dict(data["current_track"], dlna_device=device) if data["current_track"] else None
        next_track = Track.from_dict(data["next_track"], dlna_device=device) if data["next_track"] else None
        queue = cls(device, tracks)
        queue.current_track = current_track
        queue.next_track = next_track
        queue.is_shuffle = data.get("is_shuffle", False)
        queue.all_tracks = [Track.from_dict(track_data, dlna_device=device) for track_data in data["all_tracks"]]
        return queue
