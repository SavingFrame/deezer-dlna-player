from pydantic import BaseModel, Field


class ArtistSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    link: str = Field(...)
    picture_medium: str = Field(...)
