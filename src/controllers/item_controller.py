from typing import List

from src.entity.item import Item
from src.exceptions.input_error import InputError
from src.filter_pattern.category_filter import CategoryFilter
from src.filter_pattern.filter import Filter
from src.filter_pattern.gender_filter import GenderFilter
from src.filter_pattern.season_filter import SeasonFilter
from src.services.calculation_service import CalculationService
from src.services.item_service import ItemService


class ItemController:

    def __init__(self):
        self.item_service = ItemService()
        self.calculation_service = CalculationService()

    def get_all_items(self):
        return self.item_service.get_all_items()

    def get_category_items_and_calculation(self, category: str):
        items_result = self.item_service.get_all_items_by_category(category=category)
        return self.calculation_service.get_category_items_and_calculation(category, items_result)

    def filter_items_by(self, category: str = None, season: str = None, gender: str = None) -> List[Item]:

        if (category and not self.item_service.exists("category", category)) or (
                gender and not self.item_service.exists("gender", gender)) or (
                season and not self.item_service.exists("season", season)):
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
