import dataclasses


@dataclasses.dataclass
class Artist:
    id: str
    name: str
    picture: str | None

    @classmethod
    async def from_deezer_api_related_info(cls, api_related_info: dict):
        artist = cls(
            id=api_related_info.get('id'),
            name=api_related_info.get('name'),
            picture=api_related_info.get('picture_medium'),
        )
        return artist

    @classmethod
    async def from_deezer_api_track_info(cls, api_track_info: dict):
        artist_dict = api_track_info.get('artist')
        return await cls.from_deezer_api_related_info(artist_dict)

    @classmethod
    async def from_deezer_album_info(cls, api_album_info: dict):
        artist_dict = api_album_info.get('artist')
        return await cls.from_deezer_api_related_info(artist_dict)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'picture': self.picture,
        }

    @classmethod
    def from_dict(cls, artist_dict: dict):
        return cls(
            id=artist_dict.get('id'),
            name=artist_dict.get('name'),
            picture=artist_dict.get('picture'),
        )
