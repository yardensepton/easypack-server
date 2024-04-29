from datetime import datetime
from typing import List

from src.entity.trip import Trip
from src.entity.trip_schema import TripSchema
from src.exceptions.input_error import InputError
from src.exceptions.not_found_error import NotFoundError
from src.repositories import db_handler
from db import db


class TripService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "TRIPS")


    def create_trip(self, trip:Trip):
        # if user is not None:
        user_id = trip.user_id
        if self.availability_within_date_range(
                user_id, trip):
            inserted_trip = self.db_handler.insert_one(trip)
            return inserted_trip

    def get_trip_by_id(self, trip_id:str):
        trip = self.db_handler.find_one("_id", trip_id)
        if trip is not None:
            return trip
        raise NotFoundError(obj_name="Trip", obj_id=trip_id)

    def get_trips_by_user_id(self, user_id:str):
        trips = self.db_handler.find({"user_id": user_id})
        if len(trips) != 0:
            return trips
        return []

    # todo : this func needs to be moved to the controller.
    def availability_within_date_range(self, user_id: str, new_trip: Trip) -> bool:
        trips = self.get_trips_by_user_id(user_id=user_id)
        if trips is None:
            return True

        new_trip_start = self.parse_date(new_trip.departure_date)
        new_trip_end = self.parse_date(new_trip.return_date)

        # Retrieve all trips associated with the user from the database

        # Iterate through the list of trips
        for trip in trips:
            trip_start_date = self.parse_date(trip["departure_date"])
            trip_end_date = self.parse_date(trip["return_date"])

            # Check if the trip falls within the specified date range
            if new_trip_start <= trip_start_date <= new_trip_end or new_trip_start <= trip_end_date <= new_trip_end:
                raise InputError(f"User '{user_id}' has a trip within the date range")

        # No trip found within the date range
        return True

    def parse_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")

    def delete_trips_by_user_id(self, user_id:str):
        trips = self.get_trips_by_user_id(user_id)
        if trips is not None:
            self.db_handler.delete_many({"user_id": user_id})

    def delete_trip_by_id(self, trip_id):
        trip = self.get_trip_by_id(trip_id)
        if trip is not None:
            self.db_handler.delete_one("_id", trip_id)

    def is_updated_trip_within_date_range(self, user_id: str, new_info: TripSchema,
                                          update_trip_id: str) -> bool:
        # TODO - fix this function
        """
        Check if the new trip falls within the specified date range of any existing trip, excluding the trip with the provided ID.
        """
        trips_data = self.get_trips_by_user_id(user_id)
        trips = [Trip(**trip_data) for trip_data in trips_data]

        update_trip_start_date = self.parse_date(new_info.departure_date) if new_info.departure_date else None
        update_trip_end_date = self.parse_date(new_info.return_date) if new_info.return_date else None

        for trip in trips:
            if trip.id == update_trip_id:
                continue  # Skip checking the trip we want to update

            trip_start_date = self.parse_date(trip.departure_date)
            trip_end_date = self.parse_date(trip.return_date)

            # Ensure the trip has at least one date
            if trip_start_date or trip_end_date:
                # Case 1: New trip has both dates
                if update_trip_start_date and update_trip_end_date:
                    if trip_start_date and trip_end_date:
                        if (trip_start_date <= update_trip_start_date <= trip_end_date) or (
                                trip_start_date <= update_trip_end_date <= trip_end_date):
                            return True
                    elif trip_start_date:
                        if trip_start_date <= update_trip_start_date <= update_trip_end_date:
                            return True
                    elif trip_end_date:
                        if update_trip_start_date <= trip_end_date <= update_trip_end_date:
                            return True
                # Case 2: New trip has only one date (either start or end)
                elif update_trip_start_date or update_trip_end_date:
                    if trip_start_date and update_trip_start_date:
                        if trip_start_date <= update_trip_start_date:
                            return True
                    elif trip_end_date and update_trip_end_date:
                        if trip_end_date >= update_trip_end_date:
                            return True
        return False

    def update_trip_by_id(self, new_info:TripSchema, trip_id:str):
        # adding the input values to a dict if they are not null
        trip_dict = self.get_trip_by_id(trip_id)
        trip = Trip(**trip_dict)
        print(trip.user_id)
        if new_info.return_date is not None or new_info.departure_date is not None:
            if self.is_updated_trip_within_date_range(trip.user_id, new_info, trip_id) is False:
                raise InputError("trouble with new dates given")
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }
        # updating the trip with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, trip_id)
        if updated is not None:
            return updated

    def get_all_trips(self):
        return self.db_handler.find_all()
