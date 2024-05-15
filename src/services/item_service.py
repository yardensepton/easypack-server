import logging
from typing import List

from db import db
from src.entity.item import Item
from src.exceptions.not_found_error import NotFoundError
from src.repositories.items_db import ItemsDB


class ItemService:
    def __init__(self):
        self.db_handler = ItemsDB(db, "ITEMS")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    def get_all_items_by_category(self, category: str) -> List[Item]:
        items = self.db_handler.find({"category": category})
        if items:
            return items
        raise NotFoundError(obj_name="items by category", obj_id=category)

    def get_all_items(self) -> List[Item]:
        items = self.db_handler.find_all()
        if items:
            return items
        raise NotFoundError(obj_name="items", obj_id="")

    def exists(self, key: str, value: str):
        return self.db_handler.exists(key=key, value=value)
