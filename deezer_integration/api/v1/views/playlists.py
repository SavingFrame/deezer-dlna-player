from fastapi import APIRouter

from deezer_integration.api.v1.schemas.playlists import PlaylistSchema
from deezer_integration.services.deezer import DeezerIntegration

router = APIRouter(prefix="/playlists")


@router.get("")
async def playlists(limit: int | None = None) -> list[PlaylistSchema]:
    """
    Get user playlists.
    """
    response = await DeezerIntegration().get_playlists(limit=limit)
    return response
