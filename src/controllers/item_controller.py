from typing import List

from src.entity.item import Item
from src.exceptions.input_error import InputError
from src.filter_pattern.category_filter import CategoryFilter
from src.filter_pattern.filter import Filter
from src.filter_pattern.gender_filter import GenderFilter
from src.filter_pattern.season_filter import SeasonFilter
from src.services.item_service import ItemService


class ItemController:

    def __init__(self):
        self.itemService = ItemService()

    def get_all_items(self):
        return self.itemService.get_all_items()

    def get_category_items_and_calculation(self, category: str):
        return self.itemService.get_category_items_and_calculation(category)

    def filter_items_by(self, category: str = None, season: str = None, gender: str = None) -> List[Item]:

        if (category and not self.itemService.exists("category", category)) or (
                gender and not self.itemService.exists("gender", gender)) or (
                season and not self.itemService.exists("season", season)):
           raise InputError("No items found matching the filters.")

        all_items = self.get_all_items()

        filters: List[Filter] = []
        if category:
            filters.append(CategoryFilter(category))
        if season:
            filters.append(SeasonFilter(season))
        if gender:
            filters.append(GenderFilter(gender))

        filtered_items = all_items
        for filt in filters:
            filtered_items = filt.apply(filtered_items)

        return filtered_items
