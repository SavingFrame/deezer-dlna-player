from datetime import date

from pydantic import BaseModel


class ArtistSchema(BaseModel):
    id: int
    name: str
    link: str
    picture_medium: str


class ArtistDetailSchema(ArtistSchema):
    nb_album: int
    nb_fan: int
    picture_big: str


# albums
class ArtistAlbumsSchema(BaseModel):
    id: int
    title: str
    cover_medium: str
    cover_big: str
    release_date: date
    fans: int


# Tracks


class AlbumTrackSchema(BaseModel):
    id: int
    title: str
    cover_medium: str


class ArtistTrackSchema(BaseModel):
    id: int
    name: str


class TrackSchema(BaseModel):
    id: int
    title: str
    duration: int
    rank: int
    artist: ArtistTrackSchema
    album: AlbumTrackSchema
