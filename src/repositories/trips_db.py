from src.models.trip_entity import TripEntity
from src.repositories.db_handler import DBHandler


class TripsDB(DBHandler):
    def init(self, data: dict) -> TripEntity:
        return TripEntity(**data)
