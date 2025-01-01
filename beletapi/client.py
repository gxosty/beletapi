import os
import re
import struct
import pickle
from typing import Optional, List

import requests

from .session import BeletSession
from .exceptions import *
from .api import Apis
from .models.movie import BeletMovie, BeletSeries
from .models.homepage import BeletHomepageSection
from .models.file import BeletFile
from .utils import parse_movie_url
from .downloaders.ffmpegdownloader import FFmpegDownloader
from .downloaders.downloaderbase import (
    DownloaderBase,
    DownloadProgressProtocol,
)


class BeletClient(BeletSession):
    def __init__(
        self,
        *args,
        data_file: str = "beletapidata.bin",
        downloader_cls: DownloaderBase = FFmpegDownloader,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._data_file = data_file
        self._downloader = downloader_cls(self)

        self._load_data()

    def login(self, phone: int | str) -> None:
        """Login to belet using phone number

        Phone number format:
        +993xxxxxxxx
        993xxxxxxxx
        800xxxxxxxx
        8xxxxxxxx
        xxxxxxxx

        Args:
            phone (int): phone number
        """

        phone = self._format_phone(phone)

        response = requests.Session.post(
            self,
            url=Apis.main_api.sign_in,
            json={"phone": phone},
            params={"sign_in_type": 1},
        )

        response.raise_for_status()
        response_json = response.json()

        print(response_json["msg"])
        code = input(f"Please enter the code that was sent to {phone}: ")

        response = requests.Session.post(
            self,
            url=Apis.main_api.check_code,
            json={"code": code, "token": response_json["token"]},
        )

        response.raise_for_status()

        self._refresh_token()

    def logout(self) -> None:
        """Log out from account

        Clears token and cookies
        """

        response = self.post(url=Apis.main_api.log_out)
        response.raise_for_status()

        self._clear_data()

    def get_movie(self, movie_id: int | str) -> BeletMovie:
        movie_id = self._format_movie_id(movie_id)
        response = self.get(url=Apis.film_api.movie.format(movie_id))

        response.raise_for_status()
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)

        movie = None

        if response_json["film"]["seasons"] is None:
            movie = BeletMovie(self, **response_json["film"])
        else:
            movie = BeletSeries(self, **response_json["film"])

        return movie

    def get_homepage_movies(
        self,
        offset: int = 0,
        limit: int = 3,
        h_limit: int = 12,
        type_id: int = 0,
    ) -> List[BeletHomepageSection]:
        response = self.get(
            Apis.homepage_api.home_page,
            params={
                "offset": offset,
                "limit": limit,
                "h_limit": h_limit,
                "type_id": type_id,
            },
        )

        response.raise_for_status()
        response_json = response.json()
        APIStatusError.raise_for_status(response_json)

        return list(
            BeletHomepageSection.from_data(self, data)
            for data in response_json["result"]
        )

    def download(
        self,
        file: BeletFile,
        output_filename: str,
        download_progress_callback: Optional[DownloadProgressProtocol] = None,
    ) -> str:
        return self._downloader.download(
            file,
            output_filename,
            download_progress_callback,
        )

    def _load_data(self) -> None:
        if not os.path.isfile(self._data_file):
            return

        with open(self._data_file, "rb") as file:
            data = file.read()

        token_len, cookies_len = struct.unpack(">Bi", data[0:5])

        _, _, token, cookies = struct.unpack(
            f">Bi{token_len}s{cookies_len}s",
            data,
        )

        self.token = token.decode("ascii")
        self.cookies = pickle.loads(cookies)

    def _save_data(self) -> None:
        token_len = len(self.token)
        cookies = pickle.dumps(self.cookies)
        cookies_len = len(cookies)
        data = struct.pack(
            f">Bi{token_len}s{cookies_len}s",
            token_len,
            cookies_len,
            self.token.encode("ascii"),
            cookies,
        )

        with open(self._data_file, "wb") as file:
            file.write(data)

    def _clear_data(self) -> None:
        if os.path.isfile(self._data_file):
            os.remove(self._data_file)

        self.token = None
        self.cookies.clear()

    def _refresh_token(self) -> None:
        super()._refresh_token()
        self._save_data()

    def _format_phone(self, phone: int | str) -> int:
        pattern = re.compile("[\\d]{8}$")

        if isinstance(phone, int):
            phone = str(phone)

        found = pattern.search(phone)

        if not found:
            raise ValueError(f"Wrong phone number format -> {phone}")

        return int("993" + found[0])

    def _format_movie_id(self, movie_id: int | str) -> int:
        if isinstance(movie_id, str):
            if movie_id.startswith("https://"):
                return parse_movie_url(movie_id).movie_id
            elif movie_id.isdigit():
                return int(movie_id)

        if isinstance(movie_id, int):
            return movie_id

        raise InvalidMovieIDError(movie_id)
