import math
from typing import List, Optional, Any, Coroutine

from src.models.calculation import Calculation
from src.models.item import Item
from src.exceptions.input_error import InputError
from src.models.item_for_trip import ItemForTrip
from src.services.calculation_service import CalculationService
from src.services.item_service import ItemService


class ItemController:

    def __init__(self):
        self.item_service = ItemService()
        self.calculation_service = CalculationService()

    def get_all_items(self):
        return self.item_service.get_all_items()

    def get_amount(self, category: str) -> float:
        calculation: Calculation = self.calculation_service.get_calculation(category)
        return calculation.amount_per_day

    def get_item_for_trip(self, item: Item, trip_days: int) -> ItemForTrip:
        amount: float = self.get_amount(category=item.category)
        if amount == 999:
            item_for_trip = ItemForTrip(item_name=item.name, category=item.category,
                                        amount_per_trip=1)
            return item_for_trip
        amount_per_trip = math.ceil(amount * trip_days)
        item_for_trip = ItemForTrip(item_name=item.name, category=item.category,
                                    amount_per_trip=amount_per_trip)
        return item_for_trip

    def get_category_items_and_calculation(self, category: str):
        items_result = self.item_service.get_all_items_by_category(category=category)
        return self.calculation_service.get_category_items_and_calculation(category, items_result)

    def filter_items_by(self, category: Optional[str] = None, default: Optional[bool] = None,
                        user_trip_average_temp: Optional[float] = None,
                        user_gender: Optional[str] = None) -> list[Item]:

        if ((category and not self.item_service.exists("category", category)) or (
                user_gender and not self.item_service.exists("gender", user_gender))):
            raise InputError("No items found matching the filters.")

        return self.item_service.filter_items_by(category=category,
                                                 user_trip_average_temp=user_trip_average_temp,
                                                 user_gender=user_gender,
                                                 default=default)
