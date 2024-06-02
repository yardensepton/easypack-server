from src.models.item import Item
from src.repositories.db_handler import DBHandler


class ItemsDB(DBHandler):
    def init(self, data: dict) -> Item:
        return Item(**data)
