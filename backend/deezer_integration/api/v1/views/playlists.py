from fastapi import APIRouter

from deezer_integration.api.v1.schemas.playlists import PlaylistSchema, PlaylistDetailSchema
from deezer_integration.services.deezer import DeezerIntegration

router = APIRouter(prefix="/playlists")


@router.get("")
async def playlists(limit: int | None = None) -> list[PlaylistSchema]:
    """
    Get user playlists.
    """
    response = await DeezerIntegration().get_playlists(limit=limit)
    return response


@router.get("/{playlist_id}")
async def playlist(playlist_id: int) -> PlaylistDetailSchema:
    """
    Get playlist by id.
    """
    response = await DeezerIntegration().get_playlist(playlist_id=playlist_id)
    response.update({"tracks": response.pop("tracks").get("data")})
    return response
