from pydantic import BaseModel, Field


class PlaylistSchema(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    duration: int = Field(...)
    public: bool = Field(...)
    is_loved_track: bool = Field(...)
    collaborative: bool = Field(...)
    nb_tracks: int = Field(...)
    fans: int = Field(...)
    link: str = Field(...)
    picture_medium: str = Field(...)


