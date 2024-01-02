from fastapi import APIRouter
from deezer_integration.api.v1.views import artists, playlists, tracks

router = APIRouter(prefix='/integrations/deezer')
router.include_router(artists.router)
router.include_router(playlists.router)
router.include_router(tracks.router)