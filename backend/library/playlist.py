import dataclasses
from datetime import date, datetime
from typing import TYPE_CHECKING

from deezer_integration.services.async_deezer_client import AsyncDeezer
from deezer_integration.services.deezer import deezer_integration
from library.track import Track

if TYPE_CHECKING:
    from dlna.services.dlna_device import DlnaDevice


@dataclasses.dataclass
class Playlist:
    id: str
    name: str
    duration: int
    number_tracks: int
    picture: str
    create_date: date
    creator_name: str
    tracks: list[Track]

    _dlna_device: 'DlnaDevice' = None

    async def play(self, start_from: int = None):
        self._check_dlna_device()
        player_queue = await self._dlna_device.get_player_queue()
        await player_queue.set_queue(self.tracks, start_from=start_from)
        await player_queue.play()

    def _check_dlna_device(self):
        if not self._dlna_device:
            raise ValueError('DLNA device is not set')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'number_tracks': self.number_tracks,
            'picture': self.picture,
            'create_date': self.create_date,
            'creator_name': self.creator_name,
            'tracks': [track.to_dict() for track in self.tracks]
        }

    @classmethod
    def from_dict(cls, playlist_dict: dict, dlna_device: 'DlnaDevice') -> 'Playlist':
        return cls(
            id=playlist_dict.get('id'),
            name=playlist_dict.get('name'),
            duration=playlist_dict.get('duration'),
            number_tracks=playlist_dict.get('number_tracks'),
            picture=playlist_dict.get('picture'),
            create_date=playlist_dict.get('create_date'),
            creator_name=playlist_dict.get('creator_name'),
            tracks=[Track.from_dict(track, dlna_device) for track in playlist_dict.get('tracks')]
        )

    @classmethod
    async def from_deezer_by_id(cls, playlist_id: int, dlna_device: 'DlnaDevice'):
        client = deezer_integration
        playlist = await client.get_playlist(playlist_id)
        return await cls.from_deezer_api_info(playlist, dlna_device, client.async_client)

    @classmethod
    async def from_deezer_api_info(cls, api_info: dict, dlna_device: 'DlnaDevice', deezer_async_client: AsyncDeezer):
        tracks = [
            await Track.from_deezer_api_track_info(track, dlna_device=dlna_device, _deezer_client=deezer_async_client)
            for track in api_info.get('tracks', {}).get('data', [])]
        artist = cls(
            id=api_info.get('id'),
            name=api_info.get('title'),
            duration=api_info.get('duration'),
            number_tracks=api_info.get('nb_tracks'),
            picture=api_info.get('picture_medium'),
            create_date=datetime.fromisoformat(api_info.get('creation_date')),
            creator_name=api_info.get('creator').get('name'),
            tracks=tracks,
            _dlna_device=dlna_device
        )
        return artist
