import functools
import hashlib
import re
from typing import Iterable

import requests
from Crypto.Cipher import Blowfish

from deezer_integration.exceptions import NonStreamable


class DownloadStream:
    """An iterator over chunks of a stream.

    Usage:

        >>> stream = DownloadStream("https://google.com", None)
        >>> with open('google.html', 'wb') as file:
        >>>     for chunk in stream:
        >>>         file.write(chunk)

    """

    is_encrypted = re.compile("/m(?:obile|edia)/")

    def __init__(
        self,
        url: str,
        params: dict = None,
        headers: dict = None,
        item_id: str = None,
    ):
        """Create an iterable DownloadStream of a URL.

        :param url: The url to download
        :type url: str
        :param params: Parameters to pass in the request
        :type params: dict
        :param headers: Headers to pass in the request
        :type headers: dict
        :param item_id: (Only for Deezer) the ID of the track
        :type item_id: str
        """
        self.session = self._gen_threadsafe_session(headers=headers)

        self.id = item_id
        if isinstance(self.id, int):
            self.id = str(self.id)

        if params is None:
            params = {}

        self.request = self.session.get(url, allow_redirects=True, stream=True, params=params)
        self.file_size = int(self.request.headers.get("Content-Length", 0))

        if self.file_size < 20000 and not self.url.endswith(".jpg"):
            import json

            try:
                info = self.request.json()
                try:
                    # Usually happens with deezloader downloads
                    raise NonStreamable(f"{info['error']} - {info['message']}")
                except KeyError:
                    raise NonStreamable(info)

            except json.JSONDecodeError:
                raise NonStreamable("File not found.")

    def __iter__(self) -> Iterable:
        """Iterate through chunks of the stream.

        :rtype: Iterable
        """
        if self.is_encrypted.search(self.url) is not None:
            assert isinstance(self.id, str), self.id

            blowfish_key = self._generate_blowfish_key(self.id)
            # decryptor = self._create_deezer_decryptor(blowfish_key)
            CHUNK_SIZE = 2048 * 3
            return (
                # (decryptor.decrypt(chunk[:2048]) + chunk[2048:])
                (self._decrypt_chunk(blowfish_key, chunk[:2048]) + chunk[2048:]) if len(chunk) >= 2048 else chunk
                for chunk in self.request.iter_content(CHUNK_SIZE)
            )

        return self.request.iter_content(chunk_size=1024)

    @property
    def url(self):
        """Return the requested url."""
        return self.request.url

    def __len__(self) -> int:
        """Return the value of the "Content-Length" header.

        :rtype: int
        """
        return self.file_size

    def _create_deezer_decryptor(self, key) -> Blowfish:
        return Blowfish.new(key, Blowfish.MODE_CBC, b"\x00\x01\x02\x03\x04\x05\x06\x07")

    @staticmethod
    def _generate_blowfish_key(track_id: str):
        """Generate the blowfish key for Deezer downloads.

        :param track_id:
        :type track_id: str
        """
        SECRET = "g4el58wc0zvf9na1"
        md5_hash = hashlib.md5(track_id.encode()).hexdigest()
        # good luck :)
        return "".join(
            chr(functools.reduce(lambda x, y: x ^ y, map(ord, t))) for t in zip(md5_hash[:16], md5_hash[16:], SECRET)
        ).encode()

    @staticmethod
    def _decrypt_chunk(key, data):
        """Decrypt a chunk of a Deezer stream.

        :param key:
        :param data:
        """
        return Blowfish.new(
            key,
            Blowfish.MODE_CBC,
            b"\x00\x01\x02\x03\x04\x05\x06\x07",
        ).decrypt(data)

    @staticmethod
    def _gen_threadsafe_session(
        headers: dict = None, pool_connections: int = 100, pool_maxsize: int = 100
    ) -> requests.Session:
        """Create a new Requests session with a large poolsize.

        :param headers:
        :type headers: dict
        :param pool_connections:
        :type pool_connections: int
        :param pool_maxsize:
        :type pool_maxsize: int
        :rtype: requests.Session
        """
        if headers is None:
            headers = {}

        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        session.mount("https://", adapter)
        session.headers.update(headers)
        return session
