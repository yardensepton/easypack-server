from typing import List

from src.models.item import Item
from src.filter_pattern.filter import Filter


class TempRangeFilter(Filter):
    def __init__(self, temperature: float):
        self.temperature = temperature

    def apply(self, items: List[Item]) -> List[Item]:
        filtered_items: List[Item] = []
        for item in items:
            if self.is_temperature_in_range(item):
                filtered_items.append(item)
        return filtered_items

    def is_temperature_in_range(self, item: Item) -> bool:
        if item.temp_min <= self.temperature <= item.temp_max:
            return True
        return False
