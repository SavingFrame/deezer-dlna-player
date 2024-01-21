from fastapi import APIRouter

from deezer_integration.api.v1.schemas import albums as schemas
from deezer_integration.services.deezer import DeezerIntegration

router = APIRouter(prefix="/albums")


@router.get("")
async def albums(limit: int | None = None) -> list[schemas.AlbumSchema]:
    """
    Get user albums.
    """
    response = await DeezerIntegration().get_albums(limit=limit)
    return response
