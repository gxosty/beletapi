from typing import NamedTuple, List, Dict, Any


class FilterData(NamedTuple):
    id: int
    name: str


class Filter(NamedTuple):
    name: str
    query_name: str
    data: List[FilterData]


class SortData(NamedTuple):
    id: str
    name: str


class Sort(NamedTuple):
    name: str
    name_param: str
    data: List[SortData]


class SearchFilters:
    def __init__(self, filters: List[Filter], sort: Sort) -> None:
        self._filters = filters
        self._sort = sort

    def __repr__(self) -> str:
        return __str__()

    def __str__(self) -> str:
        return (
            f"<SearchFilters: filters={len(self.filters)} sortable={self._sort != {}}>"
        )

    @staticmethod
    def from_data(json_data: Dict[str, Any]) -> "SearchFilters":
        data = json_data.get("data", [])
        data_sort = json_data.get("data_sort", {})

        filters = []

        for d in data:
            filter_data = []

            for d2 in d["data"]:
                filter_data.append(FilterData(id=d2["id"], name=d2["name"]))

            filters.append(
                Filter(name=d["name"], query_name=d["query_name"], data=filter_data)
            )

        sort = None

        if data_sort:
            sort_data = []

            for d in data_sort["data"]:
                sort_data.append(SortData(id=d["id"], name=d["name"]))

            sort = Sort(
                name=data_sort["name"],
                name_param=data_sort["name_param"],
                data=sort_data,
            )

        return SearchFilters(filters=filters, sort=sort)

    @property
    def filters(self) -> List[Filter]:
        return self._filters

    @property
    def sort(self) -> Sort:
        return self._sort
