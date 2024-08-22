from typing import List, Optional

from db import db
from src.models.item import Item
from src.exceptions.not_found_error import NotFoundError
from src.repositories.items_db import ItemsDB


class ItemService:
    def __init__(self):
        self.db_handler = ItemsDB(db, "ITEMS")

    def get_all_items_by_category(self, category: str) -> List[Item]:
        items = self.db_handler.find({"category": category})
        if items:
            return items
        raise NotFoundError(obj_name="items by category", obj_id=category)

    def filter_items_by(self, category: Optional[str] = None, default: Optional[bool] = None,
                        user_trip_average_temp: Optional[float] = None,
                        user_gender: Optional[str] = None) -> List[Item]:
        query = {}
        if category:
            query["category"] = category
        if user_trip_average_temp:
            query["temp_max"] = {"$gte": user_trip_average_temp}
            query["temp_min"] = {"$lte": user_trip_average_temp}
        if user_gender:
            query["gender"] = {"$in": [user_gender, "all"]}
        if default is not None:
            query["default"] = default

        return self.db_handler.find(query)

    def get_all_items(self) -> List[Item]:
        items = self.db_handler.find_all()
        if items:
            return items
        raise NotFoundError(obj_name="items", obj_id="")

    def get_item_by_name(self, name: str) -> Item:
        item = self.db_handler.find_one("name", name)
        if item:
            return item
        raise NotFoundError(obj_name="item", obj_id="")

    def exists(self, key: str, value: str | float):
        return self.db_handler.exists(key=key, value=value)
