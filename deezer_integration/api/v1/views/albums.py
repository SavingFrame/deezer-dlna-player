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


@router.get("/{album_id}")
async def album(album_id: int) -> schemas.AlbumDetailSchema:
    """
    Get album by id.
    """
    response = await DeezerIntegration().get_album(album_id=album_id)
    response.update({'tracks': response.pop('tracks', {}).get('data', [])})
    return response
