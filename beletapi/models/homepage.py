from beletapi.session import BeletSession
from beletapi.enums import BeletHomepageSectionType
from .movie import BeletMovieFragment
from typing import Any, Dict, List


class BeletHomepageSection:
    def __init__(
        self,
        session: BeletSession,
        id: int,
        title_tk: str,
        title_ru: str,
        type: BeletHomepageSectionType,
        category_type: str,
        category_id: int,
        sort: str,
        item_size: int,
        position: int,
        content_type_id: int,
        movies: List[BeletMovieFragment],
        promotions: List[Any],
    ) -> None:
        self._session = session
        self._id = id
        self._title_tk = title_tk
        self._title_ru = title_ru
        self._type = type
        self._category_type = category_type
        self._category_id = category_id
        self._sort = sort
        self._item_size = item_size
        self._position = position
        self._content_type_id = content_type_id
        self._movies = movies
        self._promotions = promotions

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<BeletHomepageSection: title_ru='{self.title_ru}' | {len(self.movies)} movies>"

    @staticmethod
    def from_data(session, data: Dict[str, Any]):
        movies = []
        for movie in data.get("movies", []):
            movies.append(BeletMovieFragment(session, **movie))

        data["movies"] = movies
        return BeletHomepageSection(session, **data)

    @property
    def id(self):
        return self._id

    @property
    def title_tk(self):
        return self._title_tk

    @property
    def title_ru(self):
        return self._title_ru

    @property
    def type(self):
        return self._type

    @property
    def category_type(self):
        return self._category_type

    @property
    def category_id(self):
        return self._category_id

    @property
    def sort(self):
        return self._sort

    @property
    def item_size(self):
        return self._item_size

    @property
    def position(self):
        return self._position

    @property
    def content_type_id(self):
        return self._content_type_id

    @property
    def movies(self):
        return self._movies

    @property
    def promotions(self):
        return self._promotions
