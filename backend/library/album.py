import dataclasses
from datetime import date
from typing import List, TYPE_CHECKING, Optional

from config import settings
from deezer_integration.services.async_deezer_client import AsyncDeezer
from deezer_integration.services.deezer import deezer_integration
from library.artist import Artist

if TYPE_CHECKING:
    from library.track import Track
    from dlna.services.dlna_device import DlnaDevice


@dataclasses.dataclass
class Album:
    id: str
    title: str
    artist: Artist
    cover: str
    tracklist_url: str
    release_date: date | None = None

    dlna_device: Optional['DlnaDevice'] = None

    _tracks: list['Track'] | None = None
    _deezer_client: AsyncDeezer | None = None

    async def get_deezer_client(self) -> AsyncDeezer:
        if not self._deezer_client:
            deezer_client = await self._get_deezer_client()
            self._deezer_client = deezer_client
        return self._deezer_client

    @staticmethod
    async def _get_deezer_client():
        deezer_client = AsyncDeezer()
        await deezer_client.login_via_arl(settings.DEEZER_ARL)
        return deezer_client

    async def get_tracks(self) -> list['Track']:
        if self._tracks:
            return self._tracks
        deezer_client = await self.get_deezer_client()
        response = await deezer_client.api.get_album_tracks(self.id)
        tracks = await self._get_tracks_instances(
            response.get('data'),
            artist=self.artist,
            album=self,
            dlna_device=self.dlna_device,
            deezer_client=deezer_client,
        )
        return tracks

    @classmethod
    async def _get_tracks_instances(
        cls,
        tracks: list[dict],
        artist: Artist,
        album: 'Album',
        dlna_device: Optional['DlnaDevice'] = None,
        deezer_client: AsyncDeezer | None = None,
    ) -> List['Track']:
        from library.track import Track
        deezer_client = deezer_client or await cls._get_deezer_client()
        track_instances = [Track(
            id=track.get('id'),
            title=track.get('title'),
            artist=artist,
            album=album,
            duration=track.get('duration'),
            dlna_device=dlna_device,
            _deezer_client=deezer_client,
        ) for track in tracks]
        return track_instances

    def _check_dlna_device(self):
        if not self.dlna_device:
            raise ValueError('DLNA device is not set')

    async def play(self, start_from: int | None = None):
        self._check_dlna_device()
        tracks = await self.get_tracks()
        player_queue = await self.dlna_device.get_player_queue()
        await player_queue.set_queue(tracks, start_from=start_from)
        await player_queue.play()

    @classmethod
    async def from_deezer_api_track_info(
        cls,
        api_track_info: dict,
        artist: Artist | None = None,
    ) -> 'Album':
        album_dict = api_track_info.get('album')
        artist = artist or await Artist.from_deezer_api_track_info(api_track_info)
        release_date = album_dict.get('release_date')
        album = cls(
            id=album_dict.get('id'),
            title=album_dict.get('title'),
            cover=album_dict.get('cover_medium'),
            artist=artist,
            tracklist_url=album_dict.get('tracklist'),
            release_date=date.fromisoformat(release_date) if release_date else None,
        )
        return album

    @classmethod
    async def from_deezer_api_album_info(
        cls,
        api_album_info: dict,
        dlna_device: Optional['DlnaDevice'] = None,
        deezer_client: AsyncDeezer | None = None
    ) -> 'Album':
        artist = await Artist.from_deezer_album_info(api_album_info)
        album = cls(
            id=api_album_info.get('id'),
            title=api_album_info.get('title'),
            cover=api_album_info.get('cover_medium'),
            artist=artist,
            tracklist_url=api_album_info.get('tracklist'),
            release_date=date.fromisoformat(api_album_info.get('release_date')),
            dlna_device=dlna_device,
            _deezer_client=deezer_client,
        )
        tracks_list = api_album_info.get('tracks').get('data')
        await cls._get_tracks_instances(
            tracks_list,
            artist,
            album,
            dlna_device=dlna_device,
            deezer_client=deezer_client
        )
        return album

    @classmethod
    async def from_deezer_by_id(cls, album_id: str, dlna_device: 'DlnaDevice') -> 'Album':
        client = deezer_integration
        album_info = await client.get_album(int(album_id))
        album = await cls.from_deezer_api_album_info(
            album_info,
            dlna_device=dlna_device,
            deezer_client=client.async_client
        )
        return album

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist.to_dict(),
            'cover': self.cover,
            'tracklist_url': self.tracklist_url,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            '_tracks': self._tracks,
        }

    @classmethod
    def from_dict(cls, album_dict: dict, dlna_device: Optional['DlnaDevice'] = None) -> 'Album':
        artist = Artist.from_dict(album_dict.get('artist'))
        release_date = album_dict.get('release_date')
        album = cls(
            id=album_dict.get('id'),
            title=album_dict.get('title'),
            cover=album_dict.get('cover'),
            artist=artist,
            tracklist_url=album_dict.get('tracklist_url'),
            release_date=date.fromisoformat(release_date) if release_date else None,
            _tracks=album_dict.get('_tracks'),
            dlna_device=dlna_device,
        )
        return album
