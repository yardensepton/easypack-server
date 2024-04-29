import logging
from typing import List

from db import db
from src.entity.item_boundary import ItemBoundary
from src.exceptions.not_found_error import NotFoundError
from src.repositories import db_handler
from src.services.calculation_service import CalculationService


class ItemService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "ITEMS")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    def get_all_items_by_category(self, category:str):
        items = self.db_handler.find({"category": category})
        if items:
            return items
        raise NotFoundError(obj_name="items by category",obj_id=category)

    def get_all_items(self):
        items = self.db_handler.find_all()
        if items:
            return items
        raise NotFoundError(obj_name="items",obj_id="")

    def get_category_items_and_calculation(self, category:str):
        items_result = self.get_all_items_by_category(category=category)
        calculation_result = CalculationService().get_calculations(category)
        if len(items_result) == 0:
            raise NotFoundError(obj_name="items by category", obj_id=category)
        if len(calculation_result) == 0:
            raise NotFoundError(obj_name="calculation under the category",obj_id=category)

        item_boundaries = []
        amount_per_day = calculation_result.get("amountPerDay")
        for item in items_result:
            item_boundary = ItemBoundary(category=category, name=item["name"], amount=amount_per_day)
            item_boundaries.append(item_boundary)

        return item_boundaries


    def exists(self, key: str, value: str):
        return self.db_handler.exists(key=key, value=value)
