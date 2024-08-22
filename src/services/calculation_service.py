from typing import List, Optional

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
        """
                Retrieve a calculation by category from the database.

                Args:
                    category (str): The category of the calculation to retrieve.

                Returns:
                    Calculation: The calculation object associated with the category.

                Raises:
                    NotFoundError: If no calculation is found for the given category.
                """
        calculation: Calculation = self.db_handler.find_one("category", category)
        if calculation:
            return calculation
        raise NotFoundError(obj_name="Calculation under the category", obj_id=category)

    def filter_calculation(self, category: Optional[str] = None, activity: Optional[bool] = None) -> List[Calculation]:
        """
                Filter calculations based on optional category and activity status.

                Args:
                    category (Optional[str]): The category to filter by.
                    activity (Optional[bool]): The activity status to filter by.

                Returns:
                    List[Calculation]: A list of calculations that match the filter criteria.
                """
        query = {}

        if category:
            query["category"] = category
        if activity is not None:
            query["activity"] = activity

        return self.db_handler.find(query)

    def get_category_items_and_calculation(self, category: str, items_result: List[Item]) -> List[ItemAndCalculation]:
        """
               Get items and their associated calculations for a given category.

               Args:
                   category (str): The category for which to retrieve items and calculations.
                   items_result (List[Item]): The list of items to associate with the calculation.

               Returns:
                   List[ItemAndCalculation]: A list of ItemAndCalculation objects with category, name, activity, and amount per day.

               Raises:
                   NotFoundError: If no items or calculation is found for the given category.
               """
        calculation: Calculation = self.get_calculation(category=category)

        if not items_result:
            raise NotFoundError(obj_name="items by category", obj_id=category)
        if not calculation:
            raise NotFoundError(obj_name="calculation under the category", obj_id=category)

        amount_per_day = calculation.amount_per_day
        items_and_calc: List[ItemAndCalculation] = []

        for item in items_result:
            item_and_calc: ItemAndCalculation = ItemAndCalculation(category=category, name=item.name,
                                                                   activity=calculation.activity,
                                                                   amount_per_day=amount_per_day)
            items_and_calc.append(item_and_calc)

        return items_and_calc
