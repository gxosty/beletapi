import json


class InvalidTokenError(Exception):
    def __init__(self, token) -> None:
        super().__init__("Token is invalid -> {}. Are you not logged in?".format(token))


class UnauthorizedError(Exception):
    def __init__(self, message=None) -> None:
        msg = "User isn't authorized, please login first!"

        if message:
            if '"msg":' in message:
                msg += " " + json.loads(message)["msg"]
            else:
                msg += " " + message

        super().__init__(msg)


class InvalidMovieIDError(Exception):
    def __init__(self, movie_id) -> None:
        super().__init__("Invalid movie id was passed -> {}".format(movie_id))


class APIStatusError(Exception):
    def __init__(self, message) -> None:
        super().__init__("API Status error -> {}".format(message))

    @staticmethod
    def raise_for_status(json_data) -> None:
        if json_data["status"] == "error":
            raise APIStatusError(json_data["message"])
