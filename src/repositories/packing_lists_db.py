from src.entity.packing_list import PackingList
from src.repositories.db_handler import DBHandler


class PackingListsDB(DBHandler):
    def init(self, data: dict) -> PackingList:
        return PackingList(**data)
