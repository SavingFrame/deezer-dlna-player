import binascii
import hashlib
import html.parser
import logging
import os
from typing import Dict, Any, Optional

from Crypto.Cipher import AES
from fastapi import HTTPException
from pathvalidate import sanitize_filepath

import deezer
from config import settings
from deezer_integration.services.stream import DownloadStream
from deezer_integration.utils import get_extension

logger = logging.getLogger(__name__)


class ScriptExtractor(html.parser.HTMLParser):
    """ extract <script> tag contents from a html page """

    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.scripts = []
        self.curtag = None

    def handle_starttag(self, tag, attrs):
        self.curtag = tag.lower()

    def handle_data(self, data):
        if self.curtag == "script":
            self.scripts.append(data)

    def handle_endtag(self, tag):
        self.curtag = None


class DeezerDownloader:

    def __init__(self, track_id: str, deezer_client: deezer.Deezer | None = None):
        self.client = deezer_client or deezer.Deezer()
        self.login()
        self.track_id = track_id
        self.track_info = None

    def login(self):
        if self.client.logged_in:
            return
        success = self.client.login_via_arl(settings.DEEZER_ARL)
        if not success:
            raise HTTPException(status_code=401, detail="Unauthorized: No access token available")

    def get_gw_track_info(self):
        if getattr(self, "track_info", None):
            return self.track_info
        response = self.client.gw.get_track(self.track_id)
        logger.info(f"Track info: {response}")
        self.track_info = response
        return response

    def _get_encrypted_file_url(
        self, meta_id: str, track_hash: str, media_version: str
    ):
        format_number = 1

        url_bytes = b"\xa4".join(
            (
                track_hash.encode(),
                str(format_number).encode(),
                str(meta_id).encode(),
                str(media_version).encode(),
            )
        )
        url_hash = hashlib.md5(url_bytes).hexdigest()
        info_bytes = bytearray(url_hash.encode())
        info_bytes.extend(b"\xa4")
        info_bytes.extend(url_bytes)
        info_bytes.extend(b"\xa4")
        # Pad the bytes so that len(info_bytes) % 16 == 0
        padding_len = 16 - (len(info_bytes) % 16)
        info_bytes.extend(b"." * padding_len)

        logger.debug("Info bytes: %s", info_bytes)
        path = self._gen_url_path(info_bytes)
        logger.debug(path)
        return f"https://e-cdns-proxy-{track_hash[0]}.dzcdn.net/mobile/1/{path}"

    def _gen_url_path(self, data):
        return binascii.hexlify(
            AES.new("jo6aey6haid2Teih".encode(), AES.MODE_ECB).encrypt(data)
        ).decode("utf-8")

    async def get_file_url(self, quality: int = 2) -> tuple[dict, dict]:
        dl_info: Dict[str, Any] = {"quality": quality, "id": self.track_id}
        quality_map = [
            (9, "MP3_128"),  # quality 0
            (3, "MP3_320"),  # quality 1
            (1, "FLAC"),  # quality 2
        ]
        track_info = self.get_gw_track_info()
        dl_info["fallback_id"] = track_info.get("FALLBACK", {}).get("SNG_ID")
        _, format_str = quality_map[quality]
        dl_info["quality_to_size"] = [
            int(track_info.get(f"FILESIZE_{format}", 0)) for _, format in quality_map
        ]
        token = track_info["TRACK_TOKEN"]
        try:
            url = self.client.get_track_url(token, format_str)
        except deezer.WrongLicense:
            raise HTTPException(
                401,
                "The requested quality is not available with your subscription. "
                "Deezer HiFi is required for quality 2. Otherwise, the maximum "
                "quality allowed is 1."
            )

        if url is None:
            url = self._get_encrypted_file_url(
                self.track_id, track_info["MD5_ORIGIN"], track_info["MEDIA_VERSION"]
            )
        dl_info["url"] = url
        return dl_info, track_info

    def _get_path(self, dl_info: dict, track_info) -> tuple[str, bool]:
        """Do preprocessing before downloading items.

        It creates the directories, downloads cover art, and (optionally)
        downloads booklets.

        """
        folder = settings.MEDIA_PATH
        artist_name = track_info.get('ART_NAME', 'Unknown Artist')
        album_name = track_info.get('ALB_TITLE', 'Unknown Album')
        track_title = track_info.get('SNG_TITLE', dl_info.get('id'))
        track_number = str(track_info.get('TRACK_NUMBER', 1)).zfill(2)
        folder_path = os.path.join(
            folder,
            artist_name,
            album_name,
        )
        folder_path = sanitize_filepath(folder_path, platform="auto")
        filename = f"{track_number} - {track_title}" + get_extension(dl_info["quality"])
        filename = sanitize_filepath(filename, platform="auto")

        os.makedirs(folder_path, exist_ok=True)

        filepath = os.path.join(folder_path, filename)
        file_already_exists = os.path.isfile(filepath)
        if file_already_exists:
            logger.info("File already exists: %s", filepath)
        return filepath, file_already_exists

    async def download_song(self):
        dl_info, track_info = await self.get_file_url()
        filepath, file_exists = self._get_path(dl_info, track_info)
        if file_exists:
            return filepath
        stream = DownloadStream(dl_info["url"], item_id=dl_info.get('id'))
        # stream_size = len(stream)
        # stream_quality = dl_info["size_to_quality"][stream_size]
        with open(filepath, "wb") as file:
            for chunk in stream:
                file.write(chunk)
        return filepath

    @staticmethod
    def _quality_id_from_filetype(filetype: str) -> Optional[int]:
        return {
            "MP3_128": 0,
            "MP3_256": 0,
            "MP3_320": 1,
            "FLAC": 2,
        }.get(filetype)

# deezer_downloader = DeezerDownloader()
