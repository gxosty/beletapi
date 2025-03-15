from beletapi.session import BeletSession
from .moviebase import BeletMovieBase
from .movie import BeletMovieFragment


class BeletSearchResult:
    def __init__(self, session: BeletSession,  movies: list[BeletMovieBase]): # type: ignore
        self._session = session
        self._movies = movies

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<BeletSearchResult: {len(self._movies)} results>"

    @staticmethod
    def from_data(session: BeletSession, data: dict) -> "BeletSearchResult": # type: ignore
        movies = []

        for movie in data.get("films", []):
            movies.append(BeletMovieFragment(session, **movie))

        return BeletSearchResult(session, movies)

    @property
    def movies(self):
        return self._movies