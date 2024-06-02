from typing import List

from src.models.item import Item
from src.filter_pattern.filter import Filter


class CategoryFilter(Filter):
    def __init__(self, category):
        self.category = category

    def apply(self, items: List[Item]) -> List[Item]:
        return [item for item in items if item.category == self.category]
