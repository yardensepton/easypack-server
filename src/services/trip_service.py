from src.entity.trip import Trip
from src.entity.trip_schema import TripSchema
from src.exceptions.not_found_error import NotFoundError
from src.repositories import db_handler
from db import db


class TripService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "TRIPS")

    def create_trip(self, trip: Trip):
        return self.db_handler.insert_one(trip)

    def get_trip_by_id(self, trip_id: str):
        trip = self.db_handler.find_one("_id", trip_id)
        if trip is not None:
            return trip
        raise NotFoundError(obj_name="Trip", obj_id=trip_id)

    def get_trips_by_user_id(self, user_id: str):
        trips = self.db_handler.find({"user_id": user_id})
        if len(trips) != 0:
            return trips
        return []

    def delete_trips_by_user_id(self, user_id: str):
        trips = self.get_trips_by_user_id(user_id)
        if trips is not None:
            self.db_handler.delete_many({"user_id": user_id})

    def delete_trip_by_id(self, trip_id):
        trip = self.get_trip_by_id(trip_id)
        if trip is not None:
            self.db_handler.delete_one("_id", trip_id)

    def update_trip_by_id(self, new_info: TripSchema, trip_id: str)->Trip:
        # adding the input values to a dict if they are not null
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }
        # updating the trip with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, trip_id)

        if updated is not None:
            return updated
        raise NotFoundError(obj_name="trip", obj_id=trip_id)


    def get_all_trips(self):
        return self.db_handler.find_all()
