from typing import Optional

from pydantic import BaseModel, Field

from deezer_integration.api.v1.schemas.tracks import ArtistSchema


class AlbumSchema(BaseModel):
    id: int
    title: str
    link: str
    cover_medium: str
    artist: ArtistSchema
    nb_tracks: int
    duration: Optional[int] = Field(None, description="Duration in seconds")
    release_date: str


class AlbumTrackSchema(BaseModel):
    id: int
    title: str
    duration: int


class AlbumDetailSchema(AlbumSchema):
    cover_big: str
    fans: Optional[int] = None
    tracks: list[AlbumTrackSchema]
