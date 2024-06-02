from typing import List

from src.models.item import Item
from src.filter_pattern.filter import Filter


class SeasonFilter(Filter):
    def __init__(self, season):
        self.season = season

    def apply(self, items: List[Item]) -> List[Item]:
        return [item for item in items if item.season == self.season or item.season == "all"]
