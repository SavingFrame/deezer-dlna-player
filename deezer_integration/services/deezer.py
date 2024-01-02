import logging

import deezer
import httpx
from fastapi import HTTPException

from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")


class DeezerIntegration:
    def __init__(self):
        self.client = deezer.Deezer()
        self.login()

    def login(self):
        success = self.client.login_via_arl(settings.DEEZER_ARL)
        if not success:
            raise HTTPException(status_code=401, detail="Unauthorized: No access token available")

    async def get_playlists(self, limit: None | int = None):
        limit = limit or 25
        return self.client.api.get_user_playlists(
            user_id=self.client.current_user.get('id'),
            limit=limit
        ).get('data')

    async def get_artists(self, limit: None | int = None):
        limit = limit or 25
        return self.client.api.get_user_artists(
            user_id=self.client.current_user.get('id'),
            limit=limit
        ).get('data')

    async def get_favorite_tracks(self, limit: None | int = None):
        limit = limit or 25
        return self.client.api.get_user_tracks(
            user_id=self.client.current_user.get('id'),
            limit=limit
        ).get('data')

    async def search_tracks(self, query: str):
        """
        Search for music on Deezer.
        """
        if not self.DEEZER_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized: No access token available")
        url = self.DEEZER_API + "/search"
        params = {"q": query}
        headers = {"Authorization": f"Bearer {self.DEEZER_TOKEN}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to perform search_tracks")

            return response.json()



