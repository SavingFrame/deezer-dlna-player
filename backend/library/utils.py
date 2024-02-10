import posixpath
import urllib.parse

from config import settings


def filepath_to_url(file_path: str) -> str:
    file_path = file_path.replace(settings.MEDIA_PATH, "", 1)
    if file_path.startswith("/"):
        file_path = file_path[1:]
    url = posixpath.join(settings.MEDIA_URL, urllib.parse.quote(file_path))
    return url
