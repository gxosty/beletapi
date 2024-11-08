from typing import Optional, Dict, List, Any

from beletapi.session import BeletSession
from beletapi.enums import BeletCategory


class BeletMovieBase:
    """Base movie class that only holds data

    Other classes should inherit this class and add
    other functionality
    """

    def __init__(self, session: BeletSession, **kwargs) -> None:
        self._session = session

        # ID of movie or series
        self.id: int = kwargs.get("id", None)

        # Name
        self.name: str = kwargs.get("name", None)

        # Age rating
        self.age: int = kwargs.get("age", None)

        # Release year
        self.year: int = kwargs.get("year", None)

        # Duration in seconds
        self.duration: float | str = kwargs.get("duration", None)

        # Thumbnails
        self.thumbnails: Dict[str, Any] = kwargs.get("thumbnails", None)

        # Images
        self.images: Dict[str, Any] = kwargs.get("images", None)

        # Language
        self.language: str = kwargs.get("language", None)

        # Description
        self.description: str = kwargs.get("description", None)

        # Parent ID (What is this?)
        self.parent_id: int = kwargs.get("parent_id", None)

        # Was movie/series liked by user
        self.like: bool = kwargs.get("like", None)

        # Was movie/series disliked by user
        self.dislike: bool = kwargs.get("dislike", None)

        # Is user favorite movie/series
        self.favorites: bool = kwargs.get("favorites", None)

        # How much was watched
        self.watch_time: Optional[float] = kwargs.get("watch_time", None)

        # Type (movie or series)
        self.type_id: int = kwargs.get("type_id", None)

        # Category
        self.category_id: BeletCategory = BeletCategory(
            kwargs.get("category_id", 1)
        )

        # Rating of the movie/series in Kinopoisk
        self.rating_kp: float = kwargs.get("rating_kp", None)

        # Rating of the movie/series in IMDb
        self.rating_imdb: float = kwargs.get("rating_imdb", None)

        # Is movie/series for kids?
        self.for_kids: bool = kwargs.get("for_kids", None)

        # Genres
        self.genres: list[str] = kwargs.get("genres", None)

        # Countries
        self.countries: list[str] = kwargs.get("countries", None)

        # Actors
        self.actors: list[str] = kwargs.get("actors", None)

        # Directors
        self.directors: list[str] = kwargs.get("directors", None)

        # Seasons (+leading underscore because derived classes use it)
        self._seasons: Optional[Dict[str, Any]] = kwargs.get("seasons", None)

        # Last watched information
        self.last_episode_info: Optional[Dict[str, Any]] = kwargs.get(
            "last_episode_info", None
        )

        # Trailers
        self.trailers: Optional[List[Any]] = kwargs.get("trailers", None)

        # Media info (audios, captions...)
        self.media_info: Optional[Dict[str, Any]] = kwargs.get(
            "media_info", None
        )

        # Studios
        self.studios: Optional[List[Any]] = kwargs.get("studios", None)
