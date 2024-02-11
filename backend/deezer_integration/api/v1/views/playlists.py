from typing import Literal

from fastapi import APIRouter

from deezer_integration.api.v1.schemas.playlists import PlaylistDetailSchema, PlaylistSchema
from deezer_integration.services.deezer import deezer_integration

router = APIRouter(prefix="/playlists")


@router.get("")
async def playlists(limit: int | None = None) -> list[PlaylistSchema]:
    """
    Get user playlists.
    """
    response = await deezer_integration.get_playlists(limit=limit)
    return response


@router.get("/{playlist_id}")
async def playlist(playlist_id: int, tracks_ordering: Literal["asc", "desc"] = "asc") -> PlaylistDetailSchema:
    """
    Get playlist by id.
    """
    response = await deezer_integration.get_playlist(playlist_id=playlist_id, tracks_ordering=tracks_ordering)
    response.update({"tracks": response.pop("tracks").get("data")})
    return response
