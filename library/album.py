import dataclasses

from library.artist import Artist


@dataclasses.dataclass
class Album:
    id: str
    title: str
    cover: str
    artist: Artist

    @classmethod
    def from_deezer_gw_track_info(cls, track_info: dict, artist: Artist | None = None):
        artist = artist or Artist.from_deezer_gw_track_info(track_info)
        album = cls(
            id=track_info.get('ALB_ID'),
            title=track_info.get('ALB_TITLE'),
            cover=track_info.get('ALB_PICTURE'),
            artist=artist,
        )
        return album
