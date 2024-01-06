import dataclasses


@dataclasses.dataclass
class Artist:
    id: str
    name: str
    picture: str

    @classmethod
    def from_deezer_gw_track_info(cls, track_info: dict):
        artist = track_info.get('ARTISTS')[0]
        artist = cls(
            id=artist.get('ART_ID'),
            name=artist.get('ART_NAME'),
            picture=artist.get('ART_PICTURE'),
        )
        return artist
