from fastapi import APIRouter

from deezer_integration.api.v1.schemas import search as schemas
from deezer_integration.services.deezer import deezer_integration

router = APIRouter(prefix="/search")


@router.get("/tracks/{query}")
async def search_tracks(query: str, limit: int = 5, offset=0) -> list[schemas.TrackSchema]:
    """
    Search tracks.
    """
    response = await deezer_integration.search_tracks(query=query, limit=limit)
    return response


@router.get("/albums/{query}")
async def search_albums(query: str, limit: int = 5, offset=0) -> list[schemas.AlbumSchema]:
    """
    Search albums.
    """
    response = await deezer_integration.search_albums(query=query, limit=limit)
    return response


@router.get("/artists/{query}")
async def search_artists(query: str, limit: int = 5, offset=0) -> list[schemas.ArtistSchema]:
    """
    Search artists.
    """
    response = await deezer_integration.search_artists(query=query, limit=limit)
    return response
