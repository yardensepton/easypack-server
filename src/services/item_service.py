import logging
from typing import List

from db import db
from src.entity.item_boundary import ItemBoundary
from src.exceptions.item_not_found_error import ItemNotFoundError
from src.filter_pattern.category_filter import CategoryFilter
from src.filter_pattern.gender_filter import GenderFilter
from src.filter_pattern.season_filter import SeasonFilter
from src.repositories import db_handler
from src.services.calculation_service import CalculationService


class ItemService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "ITEMS")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    def get_all_items_by_category(self, category):
        items = self.db_handler.find({"category": category})
        if items:
            return items
        raise ItemNotFoundError(category=category)

    def get_all_items_by_season(self, season):
        items = self.db_handler.find({"season": season})
        if items:
            return items
        raise ItemNotFoundError(season=season)

    def get_all_items(self):
        items = self.db_handler.find_all()
        if items:
            return items
        raise ItemNotFoundError()

    def get_category_items_and_calculation(self, category) -> List[ItemBoundary]:
        items_result = self.get_all_items_by_category(category=category)
        calculation_result = CalculationService().get_calculations(category)

        item_boundaries = []
        amount_per_day = calculation_result.get("amountPerDay")
        for item in items_result:
            item_boundary = ItemBoundary(category=category, name=item["name"], amount=amount_per_day)
            item_boundaries.append(item_boundary)

        return item_boundaries

    def get_all_items_by_gender(self, gender):
        items = self.db_handler.find({"gender": gender})
        if items:
            return items
        raise ItemNotFoundError(gender=gender)


