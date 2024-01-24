from pydantic import BaseModel


# Track search schemas
class TrackArtistSchema(BaseModel):
    id: int
    name: str


class TrackAlbumSchema(BaseModel):
    id: int
    title: str
    cover_medium: str


class TrackSchema(BaseModel):
    id: int
    title: str
    duration: int
    artist: TrackArtistSchema
    album: TrackAlbumSchema


# Album search schemas

class AlbumSchema(BaseModel):
    id: int
    title: str
    cover_medium: str
    nb_tracks: int
    record_type: str
    artist: TrackArtistSchema


# Artist search schemas

class ArtistSchema(BaseModel):
    id: int
    name: str
    picture_medium: str
    nb_album: int
    nb_fan: int
