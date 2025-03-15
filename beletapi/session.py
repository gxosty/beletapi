import base64
import time
from typing import Callable, Optional, Dict

import requests

from .api import Apis
from .exceptions import *


class BeletSession(requests.Session):
    """Core object for communicating with belet REST api directly

    This object is only used to get raw data from server,
    it just wraps the `requests.Session` object providing
    useful data to server such as session token and cookies
    """

    """Session token"""
    _token: Optional[str]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._token = None

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token) -> None:
        self._token = token

    def get_token_expiration_date(self) -> int:
        """Get timestamp of token expiration time

        Returns time after which token expires

        Returns:
            int: expiry time

        Raises:
            InvalidTokenError: raised if token is `None`
        """

        if not self._token:
            raise InvalidTokenError(self._token)

        s = base64.b64decode(self._token.rsplit(".", 1)[0].encode() + b"==")
        start = s.find(b"{", 1)
        return json.loads(s[start:])["exp"]

    def is_token_expired(self) -> bool:
        """Check if token is expired

        Returns:
            bool: `True` if token is expired, otherwise `False`
        """

        if not self._token:
            return True

        expiry_date = self.get_token_expiration_date()

        if time.time() > expiry_date:
            return True

        return False

    def refresh_if_expired(self) -> bool:
        """Refreshes token if it is expired

        Returns:
            bool: `True` if token was refreshed, otherwise `False`
        """

        if self.is_token_expired():
            self._refresh_token()
            return True

        return False

    def get(self, *args, **kwargs) -> requests.Response:
        """Make GET request

        Make GET request to `url` with token appended.
        Automatically refreshes token if expired.

        Args:
            All args of `requests.Request` object.
            refresh (bool): Whether token should be automatically
                            refreshed or not (default: `True`)

        Returns:
            requests.Response: response object of `requests` module
        """

        kwargs["headers"] = self._set_header_token(kwargs.get("headers", {}))

        _kwargs = kwargs.copy()
        _kwargs.pop("refresh", None)
        response = super().get(*args, **_kwargs)
        response = self._repeat_request_if_token_is_expired(
            response, self.get, *args, **kwargs
        )

        return response

    def post(self, *args, **kwargs) -> requests.Response:
        """Make POST request

        Make POST request to `url` with token appended.
        Automatically refreshes token if expired.

        Args:
            All args of `requests.Request` object.
            refresh (bool): Whether token should be automatically
                            refreshed or not (default: `True`)

        Returns:
            requests.Response: response object of `requests` module
        """

        kwargs["headers"] = self._set_header_token(kwargs.get("headers", {}))

        _kwargs = kwargs.copy()
        _kwargs.pop("refresh", None)
        response = super().post(*args, **_kwargs)
        response = self._repeat_request_if_token_is_expired(
            response, self.post, *args, **kwargs
        )

        return response

    def _set_header_token(self, headers: Dict[str, str]) -> Dict[str, str]:
        headers.setdefault("Authorization", self._token)
        return headers

    def _refresh_token(self) -> None:
        response = super().post(url=Apis.main_api.refresh)

        if response.status_code == 401:
            raise UnauthorizedError(response.text)

        response.raise_for_status()

        self.token = response.json()["token"]

    def _repeat_request_if_token_is_expired(
        self,
        response: requests.Response,
        request_function: Callable,
        *args,
        **kwargs,
    ) -> requests.Response:
        if response.status_code == 401:
            if kwargs.get("refresh", True):
                self._refresh_token()
                kwargs["refresh"] = False
                return request_function(*args, **kwargs)
            else:
                response.raise_for_status()

        return response
