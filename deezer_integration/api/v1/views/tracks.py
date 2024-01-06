from fastapi import APIRouter

from deezer_integration.api.v1.schemas.tracks import TrackSchema
from deezer_integration.services.deezer import DeezerIntegration
from deezer_integration.services.downloader import DeezerDownloader

router = APIRouter(prefix="/tracks")


@router.get("/favorites")
async def favorite_tracks(limit: int | None = None) -> list[TrackSchema]:
    """
    Get user favorite tracks.
    """
    response = await DeezerIntegration().get_favorite_tracks(limit=limit)
    return response
