import dataclasses
import datetime
from typing import TYPE_CHECKING, Optional

from deezer_integration.services.async_deezer_client import AsyncDeezer
from deezer_integration.services.downloader import DeezerDownloader
from deezer_integration.utils import get_track_filepath
from dlna.dataclasses import PlaySongInfo
from library.album import Album
from library.artist import Artist
from library.utils import filepath_to_url
from utils.upnp.dlna import CustomDmrDevice

if TYPE_CHECKING:
    from dlna.services.dlna_device import DlnaDevice


@dataclasses.dataclass
class Track:
    id: str
    title: str
    artist: Artist
    album: Album
    duration: int
    track_number: int | None = None

    dlna_device: Optional["DlnaDevice"] = None
    deezer_downloader: DeezerDownloader | None = None
    _deezer_client: AsyncDeezer | None = None

    def __post_init__(self):
        self.deezer_downloader = self.deezer_downloader or DeezerDownloader(self.id, deezer_client=self._deezer_client)

    async def play(self) -> PlaySongInfo:
        self._check_dlna_device()
        song_path = await self.deezer_downloader.download_song()
        media_url = await self._generate_media_url(song_path)
        metadata = await self.generate_dlna_metadata(self.dlna_device.dmr_device, media_url)
        playsong_info = PlaySongInfo(media_url=media_url, metadata=metadata)
        await self.dlna_device.play_song(playsong_info)
        return playsong_info

    async def get_filepath(self, download=True):
        if download:
            return await self.deezer_downloader.download_song()
        return get_track_filepath(
            artist_name=self.artist.name, album_name=self.album.title, track_name=self.title, quality=2
        )

    async def get_media_url(self, download=True) -> str:
        song_path = await self.get_filepath(download=download)
        return await self._generate_media_url(song_path)

    async def generate_play_song_info(self, download=True) -> PlaySongInfo:
        song_path = await self.get_filepath(download=download)
        media_url = await self._generate_media_url(song_path)
        metadata = await self.generate_dlna_metadata(self.dlna_device.dmr_device, media_url)
        return PlaySongInfo(media_url=media_url, metadata=metadata)

    def _check_dlna_device(self):
        if not self.dlna_device:
            raise ValueError("DLNA device is not set")

    @staticmethod
    async def _generate_media_url(file_path) -> str:
        return filepath_to_url(file_path)

    async def generate_dlna_metadata(self, dmr: CustomDmrDevice, media_url: str) -> str:
        return await dmr.construct_play_media_metadata(
            media_url=media_url,
            media_title=self.title,
            override_upnp_class="object.item.audioItem.musicTrack",
            default_mime_type="audio/flac",
            meta_data={
                "artist": self.artist.name,
                "album": self.album.title,
                "albumArtURI": self.album.cover,
                "title": self.title,
                "duration": str(datetime.timedelta(seconds=int(self.duration))),
            },
        )

    @classmethod
    async def from_deezer_gw_track_info(
        cls,
        deezer_track: dict,
        deezer_downloader: DeezerDownloader | None = None,
        dlna_device: Optional["DlnaDevice"] = None,
        artist: Artist | None = None,
        album: Album | None = None,
    ) -> "Track":
        api_track_info = await deezer_downloader.client.api.get_track(deezer_track.get("SNG_ID"))
        artist = artist or await Artist.from_deezer_api_track_info(api_track_info)
        album = album or await Album.from_deezer_api_track_info(api_track_info, artist)
        track = cls(
            id=deezer_track.get("SNG_ID"),
            title=deezer_track.get("SNG_TITLE"),
            artist=artist,
            duration=deezer_track.get("DURATION"),
            album=album,
            track_number=deezer_track.get("TRACK_NUMBER", 1),
            deezer_downloader=deezer_downloader,
            dlna_device=dlna_device,
        )
        return track

    @classmethod
    async def from_deezer_api_track_info(
        cls,
        deezer_track: dict,
        deezer_downloader: DeezerDownloader | None = None,
        dlna_device: Optional["DlnaDevice"] = None,
        artist: Artist | None = None,
        album: Album | None = None,
        _deezer_client: AsyncDeezer | None = None,
    ):
        artist = artist or await Artist.from_deezer_api_track_info(deezer_track)
        album = album or await Album.from_deezer_api_track_info(deezer_track, artist)
        track = cls(
            id=deezer_track.get("id"),
            title=deezer_track.get("title"),
            artist=artist,
            duration=deezer_track.get("duration"),
            album=album,
            track_number=deezer_track.get("track_position", 1),
            deezer_downloader=deezer_downloader,
            dlna_device=dlna_device,
            _deezer_client=_deezer_client,
        )
        return track

    @classmethod
    async def from_deezer_by_id(cls, track_id: str, dlna_device: "DlnaDevice") -> "Track":
        downloader = DeezerDownloader(track_id)
        deezer_track = await downloader.get_gw_track_info()
        return await cls.from_deezer_gw_track_info(
            deezer_track=deezer_track, deezer_downloader=downloader, dlna_device=dlna_device
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist.to_dict(),
            "album": self.album.to_dict(),
            "duration": self.duration,
            "track_number": self.track_number,
        }

    @classmethod
    def from_dict(cls, data: dict, dlna_device: "DlnaDevice") -> "Track":
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            artist=Artist.from_dict(data.get("artist")),
            album=Album.from_dict(data.get("album")),
            duration=data.get("duration"),
            track_number=data.get("track_number"),
            dlna_device=dlna_device,
        )
