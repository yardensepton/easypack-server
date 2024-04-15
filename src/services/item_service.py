import logging

from fastapi import HTTPException
from starlette import status

from db import db
from src.exceptions.item_not_found_error import ItemNotFoundError
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

    def get_all_items_by_category_and_season(self, category, season):
        items = self.db_handler.find({ "$or": [ { "category": category, "season": season }, { "category": category, "season": "all" } ] })
        if items:
            return items
        raise ItemNotFoundError(category,season)

    def get_category_items_and_calculation(self, category):
        items_result = self.get_all_items_by_category(category=category)
        calculation_result = CalculationService().get_calculations(category)


        # Extract only the names from itemList
        item_names = [item["name"] for item in items_result]

        return {
            "items": item_names,
            "amountPerDay": calculation_result.get("amountPerDay")
        }
