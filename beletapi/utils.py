import re
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
