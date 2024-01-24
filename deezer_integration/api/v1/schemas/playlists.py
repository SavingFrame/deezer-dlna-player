from pydantic import BaseModel, NaiveDatetime


class CreatorSchema(BaseModel):
    id: int
    name: str


class PlaylistSchema(BaseModel):
    id: int
    title: str
    duration: int
    public: bool
    is_loved_track: bool
    collaborative: bool
    nb_tracks: int
    fans: int
    link: str
    picture_medium: str
    creator: CreatorSchema


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
    time_add: int


class PlaylistDetailSchema(PlaylistSchema):
    picture_big: str
    creation_date: NaiveDatetime
    tracks: list[TrackSchema]
