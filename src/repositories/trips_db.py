from src.entity.trip import Trip
from src.repositories.db_handler import DBHandler


class TripsDB(DBHandler):
    def init(self, data: dict) -> Trip:
        return Trip(**data)
