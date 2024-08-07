from typing import List

from src.models.trip_entity import TripEntity
from src.models.trip_update import TripUpdate
from src.exceptions.not_found_error import NotFoundError
from db import db
from src.models.weather import WeatherDay
from src.repositories.trips_db import TripsDB


class TripService:

    def __init__(self):
        self.db_handler = TripsDB(db, "TRIPS")

    def create_trip(self, trip: TripEntity) -> TripEntity:
        return self.db_handler.insert_one(trip)

    async def get_trip_by_id(self, trip_id: str) -> TripEntity:
        trip = self.db_handler.find_one("_id", trip_id)
        if trip is not None:
            return trip
        raise NotFoundError(obj_name="Trip", obj_id=trip_id)

    async def get_trips_by_user_id(self, user_id: str) -> List[TripEntity]:
        return self.db_handler.find({"user_id": user_id})

    def delete_trips_by_user_id(self, user_id: str):
        trips = self.get_trips_by_user_id(user_id)
        if trips is not None:
            self.db_handler.delete_many({"user_id": user_id})

    def delete_trip_by_id(self, trip_id):
        trip = self.get_trip_by_id(trip_id)
        if trip is not None:
            self.db_handler.delete_one("_id", trip_id)

    def update_trip_by_id(self, new_info: TripUpdate, trip_id: str) -> TripEntity:
        # adding the input values to a dict if they are not null
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }
        # updating the trip with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, trip_id)

        if updated is not None:
            return updated
        raise NotFoundError(obj_name="trip", obj_id=trip_id)

    def get_all_trips(self) -> List[TripEntity]:
        return self.db_handler.find_all()

    def update_trip_weather_data(self, new_weather_data: List[WeatherDay], trip_id: str) -> TripEntity:
        weather_data_dicts = [weather_day.to_dict() for weather_day in new_weather_data]
        updated = self.db_handler.find_one_and_update({"weather_data": weather_data_dicts}, trip_id)
        if updated is not None:
            return updated
        raise NotFoundError(obj_name="trip", obj_id=trip_id)
