from fastapi import APIRouter

from deezer_integration.api.v1.schemas.artists import ArtistSchema
from deezer_integration.services.deezer import DeezerIntegration

router = APIRouter(prefix="/artists")


@router.get("")
async def artists(limit: int | None = None) -> list[ArtistSchema]:
    """
    Get user artists.
    """
    response = await DeezerIntegration().get_artists(limit=limit)
    return response
