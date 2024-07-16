from pymongo import IndexModel, ASCENDING

from src.models.packing_list_entity import PackingListEntity
from src.repositories.db_handler import DBHandler


class PackingListsDB(DBHandler):

    def init(self, data: dict) -> PackingListEntity:
        return PackingListEntity(**data)


