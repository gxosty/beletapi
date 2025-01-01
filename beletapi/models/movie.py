from typing import Optional, List, Dict, Any

from .moviebase import BeletMovieBase

from beletapi.session import BeletSession
from beletapi.api import Apis
from beletapi.exceptions import APIStatusError
from .file import BeletFile


class BeletMovie(BeletMovieBase):
    _files: Optional[List[BeletFile]]

    def __init__(self, session: BeletSession, **kwargs) -> None:
        super().__init__(session, **kwargs)
        self._files = None

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<BeletMovie: id={self.id} name='{self.name}'>"

    @property
    def files(self) -> List[BeletFile]:
        if self._files is not None:
            return self._files

        response = self._session.get(
            url=Apis.film_api.files.format(self.id),
            params={"type": 1},
        )

        response.raise_for_status()
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)

        self._files = [
            BeletFile(**data) for data in response.json()["sources"]
        ]

        return self._files


class BeletMovieFragment(BeletMovieBase):
    def __init__(self, session: BeletSession, **kwargs) -> None:
        super().__init__(session, **kwargs)


class BeletSeriesEpisode:
    _files: List[BeletFile]

    def __init__(
        self,
        duration: float,
        id: int,
        last_watch: Dict[str, Any],
        name: str,
        parent_id: Any,
        files: List[BeletFile],
        type_id: int,
        image: List[Dict[str, Any]],
    ):
        self.duration = duration
        self.id = id
        self.last_watch = last_watch
        self.name = name
        self.parent_id = parent_id
        self._files = files
        self.type_id = type_id
        self.image = image

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<BeletSeriesEpisode: id={self.id} name='{self.name}'>"

    @property
    def files(self) -> List[BeletFile]:
        return self._files


class BeletSeriesSeason:
    _session: BeletSession
    _episodes: Optional[List[BeletSeriesEpisode]]

    def __init__(self, session: BeletSession, id: int, name: str) -> None:
        self._session = session

        self.id = id
        self.name = name

        self._episodes = None

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<BeletSeriesSeason: id={self.id} name='{self.name}'>"

    @property
    def episodes(self) -> List[BeletSeriesEpisode]:
        if self._episodes is not None:
            return self._episodes

        response = self._session.get(
            url=Apis.film_api.episodes, params={"seasonId": self.id}
        )

        response.raise_for_status()
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)

        self._episodes = []

        for episode_info in response_json["episodes"]:
            episode_info["files"] = [
                BeletFile(**data) for data in episode_info["sources"]
            ]

            episode_info.pop("sources")
            self._episodes.append(BeletSeriesEpisode(**episode_info))

        return self._episodes

    def get_episode_by_id(self, episode_id):
        for episode in self.episodes:
            if episode.id == episode_id:
                return episode

        return None


class BeletSeries(BeletMovieBase):
    _seasons: List[BeletSeriesSeason | Dict[str, Any]]

    def __init__(self, session: BeletSession, **kwargs) -> None:
        super().__init__(session, **kwargs)  # sets `self._seasons`
        self._seasons = [
            BeletSeriesSeason(self._session, **data) for data in self._seasons
        ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<BeletSeries: id={self.id} name='{self.name}'>"

    @property
    def seasons(self) -> List[BeletSeriesSeason]:
        return self._seasons

    def get_season_by_id(self, season_id) -> BeletSeriesSeason:
        for season in self.seasons:
            if season.id == season_id:
                return season

        return None
