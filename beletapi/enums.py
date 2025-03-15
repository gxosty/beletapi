from enum import IntEnum, StrEnum


class BeletCategory(IntEnum):
    MOVIE = 1
    SERIES = 2
    ANIME = 3
    TV_SHOW = 4
    CARTOON = 5
    MUSIC = 35
    DOCUMENTAL = 36
    NEWS = 37
    SPORT = 39


class BeletHomepageSectionType(StrEnum):
    HEADER: str = "HEADER"
    CONTINUE: str = "CONTINUE"
    FAVORIE: str = "FAVORITE"
    PROMOTION: str = "PROMOTION"
    BY_CATEGORY: str = "BY_CATEGORY"