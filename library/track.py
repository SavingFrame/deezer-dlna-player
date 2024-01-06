import dataclasses

from deezer_integration.services.downloader import DeezerDownloader
from dlna.services.dlna_device import DlnaDevice, DlnaSongMetadata
from library.album import Album
from library.artist import Artist


@dataclasses.dataclass
class Track:
    id: str
    title: str
    artist: Artist
    album: Album
    duration: int

    dlna_device: DlnaDevice | None = None
    deezer_downloader: DeezerDownloader | None = None

    def __post_init__(self):
        self.deezer_downloader = self.deezer_downloader or DeezerDownloader(self.id)

    async def play(self):
        song_path = await self.deezer_downloader.download_song()
        metadata = DlnaSongMetadata(
            artist=self.artist.name,
            album=self.album.title,
            title=self.title,
        )
        await self.dlna_device.play_song(song_path, metadata=metadata)

    @classmethod
    def from_deezer_gw_track_info(
        cls,
        deezer_track: dict,
        deezer_downloader: DeezerDownloader | None = None,
        dlna_device: DlnaDevice | None = None,
        artist: Artist | None = None,
        album: Album | None = None
    ) -> 'Track':
        artist = artist or Artist.from_deezer_gw_track_info(deezer_track)
        album = album or Album.from_deezer_gw_track_info(deezer_track, artist)
        track = cls(
            id=deezer_track.get('SNG_ID'),
            title=deezer_track.get('SNG_TITLE'),
            artist=artist,
            duration=deezer_track.get('DURATION'),
            album=album,
            deezer_downloader=deezer_downloader,
            dlna_device=dlna_device,
        )
        return track

    @classmethod
    def from_deezer_by_id(cls, track_id: str, dlna_device: DlnaDevice) -> 'Track':
        downloader = DeezerDownloader(track_id)
        return cls.from_deezer_gw_track_info(
            deezer_track=downloader.get_gw_track_info(),
            deezer_downloader=downloader,
            dlna_device=dlna_device
        )
