from typing import List

from db import db
from src.models.calculation import Calculation
from src.models.item import Item
from src.models.item_and_calculation import ItemAndCalculation
from src.exceptions.not_found_error import NotFoundError
from src.repositories.calculations_db import CalculationsDB


class CalculationService:
    def __init__(self):
        self.db_handler = CalculationsDB(db, "CALCULATIONS")

    def get_calculation(self, category: str) -> Calculation:
        calculation: Calculation = self.db_handler.find_one("category", category)
        if calculation:
            return calculation
        raise NotFoundError(obj_name="Calculation under the category", obj_id=category)

    def get_category_items_and_calculation(self, category: str, items_result: List[Item]) -> List[ItemAndCalculation]:
        calculation: Calculation = self.get_calculation(category)

        if not items_result:
            raise NotFoundError(obj_name="items by category", obj_id=category)
        if not calculation:
            raise NotFoundError(obj_name="calculation under the category", obj_id=category)

        amount_per_day = calculation.amount_per_day
        item_boundaries = []

        for item in items_result:
            item_boundary = ItemAndCalculation(category=category, name=item.name, amount_per_day=amount_per_day)
            item_boundaries.append(item_boundary)

        return item_boundaries
