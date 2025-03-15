import re
import random
import datetime
from typing import NamedTuple


_movie_url_pattern = re.compile(
    "/player/(?P<type_id>\\d)/(?P<movie_id>[\\d]+)"
    "(?:\\?season\\=(?P<season_id>[\\d]+)(?:&episo"
    "de\\=(?P<episode_id>[\\d]+))?)?"
)


class BeletMovieUrlInfo(NamedTuple):
    type_id: int
    movie_id: int
    season_id: int
    episode_id: int


def parse_movie_url(url) -> BeletMovieUrlInfo:
    found = _movie_url_pattern.search(url)

    if not found:
        raise ValueError("Invalid url -> {}".format(url))

    d = found.groupdict()

    for key, value in d.items():
        if isinstance(value, str):
            d[key] = int(value)

    return BeletMovieUrlInfo(**d)


def generate_fingerprint() -> str:
    rand_str = ""

    for i in range(9):
        rand_str += "{:0>2}".format(hex(random.randint(0, 255))[2:])

    return "web" + rand_str


def format_cookie_expires(timestamp):
    """
    Formats a Unix timestamp into the HTTP cookie Expires format.

    Args:
        timestamp (int): The Unix timestamp.

    Returns:
        str: The formatted date and time string.
    """
    dt_utc = datetime.datetime.utcfromtimestamp(timestamp)
    return dt_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")
