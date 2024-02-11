import logging
from typing import Literal

from fastapi import HTTPException

from config import settings
from deezer_integration.services.async_deezer_client import AsyncDeezer

logger = logging.getLogger(__name__)


class DeezerIntegration:
    API_URL = "https://api.deezer.com/"

    def __init__(self):
        self.async_client = AsyncDeezer()

    async def login(self):
        if self.async_client.logged_in:
            return
        success = await self.async_client.login_via_arl(settings.DEEZER_ARL)
        if not success:
            raise HTTPException(status_code=401, detail="Unauthorized: No access token available")

    async def get_playlists(self, limit: None | int = None, add_flow: bool = True):
        await self.login()
        limit = limit or 25
        response = await self.async_client.api.get_user_playlists(
            user_id=self.async_client.current_user.get("id"), limit=limit
        )
        return response.get("data")

    async def get_playlist(self, playlist_id: int, tracks_ordering: Literal["asc", "desc"] = "asc"):
        await self.login()
        response = await self.async_client.api.get_playlist(playlist_id)
        tracks = response.get("tracks", {}).get("data", [])
        if tracks_ordering == "desc":
            tracks = sorted(tracks, key=lambda x: x.get("time_add"), reverse=True)
            response["tracks"]["data"] = tracks
        return response

    async def get_artists(self, limit: None | int = None):
        await self.login()
        limit = limit or 25
        response = await self.async_client.api.get_user_artists(
            user_id=self.async_client.current_user.get("id"), limit=limit
        )
        return response.get("data")

    async def get_artist(self, artist_id: int):
        await self.login()
        response = await self.async_client.api.get_artist(artist_id)
        return response

    async def get_artist_albums(self, artist_id: int):
        await self.login()
        response = await self.async_client.api.get_artist_albums(artist_id)
        return response.get("data")

    async def get_artist_top(self, artist_id: int):
        await self.login()
        response = await self.async_client.api.get_artist_top(artist_id, limit=100)
        return response.get("data")

    async def get_albums(self, limit: None | int = None):
        await self.login()
        limit = limit or 25
        response = await self.async_client.api.get_user_albums(
            user_id=self.async_client.current_user.get("id"), limit=limit
        )
        return response.get("data")

    async def get_album(self, album_id: int):
        await self.login()
        response = await self.async_client.api.get_album(album_id)
        return response

    async def get_flow_tracks(self):
        await self.login()
        response = await self.async_client.api.get_user_flow(
            user_id=self.async_client.current_user.get("id"), limit=100
        )
        return response.get("data")

    async def get_favorite_tracks(self, limit: None | int = None, ordering: str = "asc"):
        await self.login()
        limit = limit or 25
        if ordering == "desc":
            response = await self.async_client.api.get_user_tracks(
                user_id=self.async_client.current_user.get("id"), limit=999
            )
            data = response.get("data")
            sorted_data = sorted(data, key=lambda x: x.get("time_add"), reverse=True)
            return sorted_data[:limit]
        else:
            response = await self.async_client.api.get_user_tracks(
                user_id=self.async_client.current_user.get("id"), limit=limit
            )

        return response.get("data")

    async def search_tracks(self, query: str, limit: int = 5):
        """
        Search for music on Deezer.
        """
        await self.login()
        response = await self.async_client.api.search(query, limit=limit)
        return response.get("data")

    async def search_albums(self, query: str, limit: int = 5):
        """
        Search for albums on Deezer.
        """
        await self.login()
        response = await self.async_client.api.search_album(query, limit=limit)
        return response.get("data")

    async def search_artists(self, query: str, limit: int = 5):
        """
        Search for artists on Deezer.
        """
        await self.login()
        response = await self.async_client.api.search_artist(query, limit=limit)
        return response.get("data")


deezer_integration = DeezerIntegration()
