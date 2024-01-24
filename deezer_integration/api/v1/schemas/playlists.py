from pydantic import BaseModel, NaiveDatetime


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


class CreatorSchema(BaseModel):
    id: int
    name: str


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
    creator: CreatorSchema
    tracks: list[TrackSchema]
