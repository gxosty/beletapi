class MetaApi(type):
    def __new__(cls, name, bases, attrs):
        if "host" not in attrs:
            raise RuntimeError("host wasn't declared")

        host = attrs.pop("host")

        for attr_name in attrs.keys():
            if attr_name.startswith("_"):
                continue

            if not host.startswith("http"):
                host = "https://" + host

            endpoint = None

            if host.endswith("/") and attrs[attr_name].startswith("/"):
                endpoint = host[:-1] + attrs[attr_name]
            elif not (host.endswith("/") or attrs[attr_name].startswith("/")):
                endpoint = host + "/" + attrs[attr_name]
            else:
                endpoint = host + attrs[attr_name]

            attrs[attr_name] = endpoint.format(**attrs)

        attrs["host"] = host

        return super().__new__(cls, name, bases, attrs)


class MainApi(metaclass=MetaApi):
    _api_version = 1

    # hostname
    host = "api.belet.tm"

    # endpoints
    sign_in = "/api/v{_api_version}/auth/sign-in"
    log_out = "/api/v{_api_version}/auth/log-out"
    check_code = "/api/v{_api_version}/auth/check-code"
    refresh = "/api/v{_api_version}/auth/refresh"


class HomepageApi(metaclass=MetaApi):
    _api_version = 1

    # host
    host = "homepage.belet.me"

    # endpoints
    home_page = "/api/v{_api_version}/home_page"


class FilmApi(metaclass=MetaApi):
    _api_version = 2

    # host
    host = "film.beletapis.com"

    # endpoint
    movie = "/api/v{_api_version}/movie/{{}}"
    files = "/api/v{_api_version}/files/{{}}"
    episodes = "/api/v{_api_version}/episodes"


class Apis:
    """Static class that centralizes all apis

    Attributes:
        main_api: Main Api
        homepage_api: Homepage Api
        film_api: Film Api
    """

    main_api = MainApi()
    homepage_api = HomepageApi()
    film_api = FilmApi()
