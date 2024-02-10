from fastapi import APIRouter

from deezer_integration.api.v1.schemas import artists as schemas
from deezer_integration.services.deezer import deezer_integration

router = APIRouter(prefix="/artists")


@router.get("")
async def artists(limit: int | None = None) -> list[schemas.ArtistSchema]:
    """
    Get user artists.
    """
    response = await deezer_integration.get_artists(limit=limit)
    return response


@router.get("/{artist_id}")
async def artist(artist_id: int) -> schemas.ArtistDetailSchema:
    """
    Get artist by id.
    """
    response = await deezer_integration.get_artist(artist_id)
    return response


@router.get("/{artist_id}/albums")
async def artist_albums(artist_id: int) -> list[schemas.ArtistAlbumsSchema]:
    """
    Get artist albums by id.
    """
    response = await deezer_integration.get_artist_albums(artist_id)
    return response


@router.get("/{artist_id}/top")
async def artist_top(artist_id: int) -> list[schemas.TrackSchema]:
    """
    Get artist top by id.
    """
    response = await deezer_integration.get_artist_top(artist_id)
    return response
