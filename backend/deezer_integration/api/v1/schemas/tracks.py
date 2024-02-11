from datetime import datetime

from pydantic import BaseModel


class AlbumSchema(BaseModel):
    id: int
    title: str
    cover_medium: str


class ArtistSchema(BaseModel):
    id: int
    name: str
    picture_medium: str


class TrackSchema(BaseModel):
    id: int
    title: str
    duration: int
    album: AlbumSchema
    artist: ArtistSchema
    time_add: datetime
