from fastapi import APIRouter

from deezer_integration.api.v1.schemas.tracks import TrackSchema
from deezer_integration.services.deezer import deezer_integration

router = APIRouter(prefix="/tracks")


@router.get("/favorites")
async def favorite_tracks(limit: int | None = None) -> list[TrackSchema]:
    """
    Get user favorite tracks.
    """
    response = await deezer_integration.get_favorite_tracks(limit=limit)
    return response
