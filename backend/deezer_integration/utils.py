import logging
import os
from string import Formatter

from pathvalidate import sanitize_filename, sanitize_filepath

from config import settings

logger = logging.getLogger(__name__)


def get_extension(quality: int) -> str:
    if quality <= 1:
        return ".mp3"
    else:
        return ".flac"


def clean_filename(fn: str, restrict=False) -> str:
    path = sanitize_filename(fn)
    if restrict:
        from string import printable

        allowed_chars = set(printable)
        path = "".join(c for c in path if c in allowed_chars)

    return path


def clean_format(formatter: str, format_info, restrict: bool = False):
    """Format track or folder names sanitizing every formatter key.

    :param formatter:
    :type formatter: str
    :param kwargs:
    """
    fmt_keys = filter(None, (i[1] for i in Formatter().parse(formatter)))
    # fmt_keys = (i[1] for i in Formatter().parse(formatter) if i[1] is not None)

    logger.debug("Formatter keys: %s", formatter)

    clean_dict = {}
    for key in fmt_keys:
        logger.debug(repr(key))
        logger.debug(format_info.get(key))
        if isinstance(format_info.get(key), (str, float)):
            logger.debug("1")
            clean_dict[key] = clean_filename(str(format_info[key]), restrict=restrict)
        elif key == "explicit":
            logger.debug("3")
            clean_dict[key] = " (Explicit) " if format_info.get(key, False) else ""
        elif isinstance(format_info.get(key), int):  # track/discnumber
            logger.debug("2")
            clean_dict[key] = f"{format_info[key]:02}"
        else:
            clean_dict[key] = "Unknown"

    return formatter.format(**clean_dict)


def get_track_filepath(artist_name: str, album_name: str, track_name: str, quality: int = 2) -> str:
    folder = settings.MEDIA_PATH
    artist_name = artist_name
    album_name = album_name
    track_title = track_name
    folder_path = os.path.join(
        folder,
        artist_name,
        album_name,
    )
    folder_path = sanitize_filepath(folder_path, platform="auto")
    filename = f"{track_title}" + get_extension(quality)
    filename = sanitize_filepath(filename, platform="auto")

    os.makedirs(folder_path, exist_ok=True)

    filepath = os.path.join(folder_path, filename)
    return filepath
