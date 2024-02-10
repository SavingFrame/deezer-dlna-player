import asyncio
import json

from deezer import Deezer, GW, API
from deezer.errors import (
    GWAPIError, ItemsLimitExceededException, PermissionException, InvalidTokenException,
    WrongParameterException, InvalidQueryException, DataException, IndividualAccountChangedNotAllowedException,
    APIError, MissingParameterException, DeezerError, WrongLicense, WrongGeolocation,
)
from deezer.gw import EMPTY_TRACK_OBJ
from deezer.utils import map_user_track
from httpx import AsyncClient, Cookies, ConnectError, TimeoutException, HTTPError


class AsyncDeezerGW(GW):

    async def get_track(self, sng_id):
        return await self.api_call('song.getData', {'SNG_ID': sng_id})

    async def get_artist_top_tracks(self, art_id, limit=100):
        tracks_array = []
        body = self.api_call('artist.getTopTrack', {'ART_ID': art_id, 'nb': limit})
        for track in body['data']:
            track['POSITION'] = body['data'].index(track)
            tracks_array.append(track)
        return tracks_array

    async def api_call(self, method, args=None, params=None) -> dict | list:
        if args is None: args = {}
        if params is None: params = {}
        if not self.api_token and method != 'deezer.getUserData': self.api_token = await self._get_token()
        p = {
            'api_version': "1.0",
            'api_token': 'null' if method == 'deezer.getUserData' else self.api_token,
            'input': '3',
            'method': method
        }
        p.update(params)
        try:
            result = await self.session.post(
                "http://www.deezer.com/ajax/gw-light.php",
                params=p,
                timeout=30,
                json=args,
                headers=self.http_headers
            )
            result_json = result.json()
        except (ConnectError, TimeoutException):
            await asyncio.sleep(2)
            return await self.api_call(method, args, params)
        if len(result_json['error']):
            if (
                result_json['error'] == {"GATEWAY_ERROR": "invalid api token"} or
                result_json['error'] == {"VALID_TOKEN_REQUIRED": "Invalid CSRF token"}
            ):
                self.api_token = await self._get_token()
                return await self.api_call(method, args, params)
            if result_json.get('payload', {}) and result_json['payload'].get('FALLBACK', {}):
                for key in result_json['payload']['FALLBACK'].keys():
                    args[key] = result_json['payload']['FALLBACK'][key]
                return await self.api_call(method, args, params)
            raise GWAPIError(json.dumps(result_json['error']))
        if not self.api_token and method == 'deezer.getUserData': self.api_token = result_json['results']['checkForm']
        return result_json['results']

    async def _get_token(self):
        token_data = await self.get_user_data()
        return token_data['checkForm']

    async def get_user_data(self):
        return await self.api_call('deezer.getUserData')

    async def get_child_accounts(self):
        return await self.api_call('deezer.getChildAccounts')

    async def get_user_artists(self, user_id, index=0, limit=25):
        return await self.api_call(f'user/{str(user_id)}/artists', {'index': index, 'limit': limit})

    async def get_tracks(self, sng_ids):
        tracks_array = []
        body = await self.api_call('song.getListData', {'SNG_IDS': sng_ids})
        errors = 0
        for i in range(len(sng_ids)):
            if sng_ids[i] != 0:
                tracks_array.append(body['data'][i - errors])
            else:
                errors += 1
                tracks_array.append(EMPTY_TRACK_OBJ)
        return tracks_array

    async def get_user_favorite_ids(self, checksum=None, limit=10000, start=0):
        return await self.api_call('song.getFavoriteIds', {'nb': limit, 'start': start, 'checksum': checksum})

    async def get_my_favorite_tracks(self, limit=25):
        ids_raw = await self.get_user_favorite_ids(limit=limit)
        ids = [x['SNG_ID'] for x in ids_raw['data']]
        if len(ids) == 0: return []
        data = await self.get_tracks(ids)
        result = []
        for (i, track) in enumerate(data):
            track = dict(track, **ids_raw['data'][i])
            result.append(map_user_track(track))
        return result

    async def get_user_profile_page(self, user_id, tab, limit=10):
        return await self.api_call('deezer.pageProfile', {'USER_ID': user_id, 'tab': tab, 'nb': limit})

    async def get_user_tracks(self, user_id, limit=25):
        user_data = await self.get_user_data()
        if user_data['USER']['USER_ID'] == user_id: return self.get_my_favorite_tracks()
        data = await self.get_user_profile_page(user_id, 'loved', limit=limit)['TAB']['loved']['data']
        result = []
        for track in data:
            result.append(map_user_track(track))
        return result


class AsyncDeezerAPI(API):

    async def search(self, query, strict=False, order=None, index=0, limit=25):
        args = self._generate_search_args(query, strict, order, index, limit)
        return await self.api_call('search', args)

    async def search_album(self, query, strict=False, order=None, index=0, limit=25):
        args = self._generate_search_args(query, strict, order, index, limit)
        return await self.api_call('search/album', args)

    async def get_album_tracks(self, album_id, index=0, limit=-1):
        return await self.api_call(f'album/{str(album_id)}/tracks', {'index': index, 'limit': limit})

    async def get_track(self, song_id):
        return await self.api_call(f'track/{str(song_id)}')

    async def search_artist(self, query, strict=False, order=None, index=0, limit=25):
        args = self._generate_search_args(query, strict, order, index, limit)
        return await self.api_call('search/artist', args)

    async def get_artist_top(self, artist_id, index=0, limit=10):
        return await self.api_call(f'artist/{str(artist_id)}/top', {'index': index, 'limit': limit})

    async def get_artist_albums(self, artist_id, index=0, limit=-1):
        return await self.api_call(f'artist/{str(artist_id)}/albums', {'index': index, 'limit': limit})

    async def get_artist(self, artist_id):
        return await self.api_call(f'artist/{str(artist_id)}')

    async def get_user_playlists(self, user_id, index=0, limit=25):
        return await self.api_call(f'user/{str(user_id)}/playlists', {'index': index, 'limit': limit})

    async def get_user_tracks(self, user_id, index=0, limit=25):
        return await self.api_call(f'user/{str(user_id)}/tracks', {'index': index, 'limit': limit})

    async def get_user_albums(self, user_id, index=0, limit=25):
        return await self.api_call(f'user/{str(user_id)}/albums', {'index': index, 'limit': limit})

    async def get_album(self, album_id):
        return await self.api_call(f'album/{str(album_id)}')

    async def get_playlist(self, playlist_id):
        return await self.api_call(f'playlist/{str(playlist_id)}')

    async def get_album_by_UPC(self, upc):
        return await self.get_album(f'upc:{upc}')

    async def api_call(self, method, args=None):
        if args is None:
            args = {}
        if self.access_token: args['access_token'] = self.access_token
        try:
            result = await self.session.get(
                "https://api.deezer.com/" + method,
                params=args,
                headers=self.http_headers,
                timeout=30
            )
            result_json = result.json()
        except (ConnectError, TimeoutException):
            await asyncio.sleep(2)
            return await self.api_call(method, args)
        if 'error' in result_json.keys():
            if 'code' in result_json['error']:
                if result_json['error']['code'] in [4, 700]:
                    await asyncio.sleep(5)
                    return self.api_call(method, args)
                if result_json['error']['code'] == 100: raise ItemsLimitExceededException(
                    f"ItemsLimitExceededException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
                if result_json['error']['code'] == 200: raise PermissionException(
                    f"PermissionException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
                if result_json['error']['code'] == 300: raise InvalidTokenException(
                    f"InvalidTokenException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
                if result_json['error']['code'] == 500: raise WrongParameterException(
                    f"ParameterException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
                if result_json['error']['code'] == 501: raise MissingParameterException(
                    f"MissingParameterException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
                if result_json['error']['code'] == 600: raise InvalidQueryException(
                    f"InvalidQueryException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
                if result_json['error']['code'] == 800: raise DataException(
                    f"DataException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
                if result_json['error']['code'] == 901: raise IndividualAccountChangedNotAllowedException(
                    f"IndividualAccountChangedNotAllowedException: {method} {result_json['error']['message'] if 'message' in result_json['error'] else ''}"
                )
            raise APIError(json.dumps(result_json['error']))
        return result_json


class AsyncDeezer(Deezer):

    def __init__(self):
        super().__init__()
        self.session = AsyncClient()
        self.gw = AsyncDeezerGW(self.session, self.http_headers)
        self.api = AsyncDeezerAPI(self.session, self.http_headers)

    async def get_track_url(self, track_token, track_format):
        tracks = await self.get_tracks_url([track_token, ], track_format)
        if len(tracks) > 0:
            if isinstance(tracks[0], DeezerError):
                raise tracks[0]
            else:
                return tracks[0]
        return None

    async def get_tracks_url(self, track_tokens, track_format):
        if not isinstance(track_tokens, list):
            track_tokens = [track_tokens, ]
        if not self.current_user.get('license_token'):
            return []
        if (track_format == "FLAC" or track_format.startswith("MP4_RA")) and not self.current_user.get(
            'can_stream_lossless'
        ) or track_format == "MP3_320" and not self.current_user.get('can_stream_hq'):
            raise WrongLicense(format)

        result = []
        try:
            request = await self.session.post(
                "https://media.deezer.com/v1/get_url",
                json={
                    'license_token': self.current_user['license_token'],
                    'media': [{
                        'type': "FULL",
                        'formats': [
                            {'cipher': "BF_CBC_STRIPE", 'format': track_format}
                        ]
                    }],
                    'track_tokens': track_tokens
                },
                headers=self.http_headers
            )
            request.raise_for_status()
            response = request.json()
        except HTTPError:
            return []

        if len(response.get('data', [])):
            for data in response['data']:
                if 'errors' in data:
                    if data['errors'][0]['code'] == 2002:
                        result.append(WrongGeolocation(self.current_user['country']))
                    else:
                        result.append(DeezerError(json.dumps(response)))
                if 'media' in data and len(data['media']):
                    result.append(data['media'][0]['sources'][0]['url'])
                else:
                    result.append(None)
        return result

    async def login_via_arl(self, arl, child=0):
        arl = arl.strip()
        if child: child = int(child)
        cookie_obj = Cookies()
        cookie_obj.set('arl', arl, domain='.deezer.com', path='/')
        self.session.cookies = cookie_obj
        user_data = await self.gw.get_user_data()
        # Check if user logged in
        if not user_data or user_data and len(user_data.keys()) == 0:
            self.logged_in = False
            return False
        if user_data["USER"]["USER_ID"] == 0:
            self.logged_in = False
            return False
        await self._post_login(user_data)
        self.change_account(child)
        self.logged_in = True
        return True

    async def _post_login(self, user_data):
        self.childs = []
        family = user_data["USER"]["MULTI_ACCOUNT"]["ENABLED"] and not user_data["USER"]["MULTI_ACCOUNT"][
            "IS_SUB_ACCOUNT"]
        if family:
            childs = await self.gw.get_child_accounts()
            for child in childs:
                if child['EXTRA_FAMILY']['IS_LOGGABLE_AS']:
                    self.childs.append(
                        {
                            'id': child["USER_ID"],
                            'name': child["BLOG_NAME"],
                            'picture': child.get("USER_PICTURE", ""),
                            'license_token': user_data["USER"]["OPTIONS"]["license_token"],
                            'can_stream_hq': user_data["USER"]["OPTIONS"]["web_hq"] or user_data["USER"]["OPTIONS"][
                                "mobile_hq"],
                            'can_stream_lossless': user_data["USER"]["OPTIONS"]["web_lossless"] or
                                                   user_data["USER"]["OPTIONS"]["mobile_lossless"],
                            'country': user_data["USER"]["OPTIONS"]["license_country"],
                            'language': user_data["USER"]["SETTING"]["global"].get("language", ""),
                            'loved_tracks': child.get("LOVEDTRACKS_ID")
                        }
                    )
        else:
            self.childs.append(
                {
                    'id': user_data["USER"]["USER_ID"],
                    'name': user_data["USER"]["BLOG_NAME"],
                    'picture': user_data["USER"].get("USER_PICTURE", ""),
                    'license_token': user_data["USER"]["OPTIONS"]["license_token"],
                    'can_stream_hq': user_data["USER"]["OPTIONS"]["web_hq"] or user_data["USER"]["OPTIONS"][
                        "mobile_hq"],
                    'can_stream_lossless': user_data["USER"]["OPTIONS"]["web_lossless"] or user_data["USER"]["OPTIONS"][
                        "mobile_lossless"],
                    'country': user_data["USER"]["OPTIONS"]["license_country"],
                    'language': user_data["USER"]["SETTING"]["global"].get("language", ""),
                    'loved_tracks': user_data["USER"].get("LOVEDTRACKS_ID")
                }
            )
