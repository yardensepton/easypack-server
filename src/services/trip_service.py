from fastapi import HTTPException
from starlette import status
from datetime import datetime

from src.entity.trip import Trip
from src.entity.update_trip import TripUpdate
from src.repositories import db_handler
from db import db


class TripService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "TRIPS")

    def validate_date(self, departure_date: str, return_date: str) -> bool:
        # Parse date strings into datetime.date objects
        date1 = self.parse_date(departure_date)
        date2 = self.parse_date(return_date)

        # Check if date2 is before date1
        if date2 < date1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Return date is before departure date")
        # Validation passed
        return True

    def create_trip(self, trip, user_id, user):
        if user is not None:
            if self.validate_date(trip.departure_date, trip.return_date) and self.availability_within_date_range(
                    user_id, trip):
                trip.user_id = user_id
                inserted_trip = self.db_handler.insert_one(trip)
                return inserted_trip


    def get_trip_by_id(self, trip_id):
        trip = self.db_handler.find_one("_id", trip_id)
        if trip is not None:
            return trip
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip {trip_id} not found")

    def get_trips_by_user_id(self, user_id):
        trips = self.db_handler.find({"user_id": user_id})
        if len(trips) != 0:
            return trips
        return None

    def get_trips_by_user_id_with_exception(self, user_id):
        trips = self.get_trips_by_user_id(user_id)
        if trips is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There are no trips for user_id {user_id}"
            )
        return trips

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
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"User {user_id} has a trip within the date range")

        # No trip found within the date range
        return True

    def parse_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # Handle invalid date format
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")

    def delete_trips_by_user_id(self, user_id):
        trips = self.get_trips_by_user_id_with_exception(user_id)
        if trips is not None:
            self.db_handler.delete_many({"user_id": user_id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user_id} not found")

    def delete_trip_by_id(self, trip_id):
        trip = self.get_trip_by_id(trip_id)
        if trip is not None:
            self.db_handler.delete_one("_id", trip_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"trip {trip_id} not found")




    def is_updated_trip_within_date_range(self, user_id: str, new_info: TripUpdate,
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

    def update_trip_by_id(self, new_info, trip_id):
        # adding the input values to a dict if they are not null
        trip_dict = self.get_trip_by_id(trip_id)
        trip = Trip(**trip_dict)
        print(trip.user_id)
        if new_info.return_date is not None or new_info.departure_date is not None:
            if self.is_updated_trip_within_date_range(trip.user_id, new_info, trip_id) is False:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"trouble with new dates given")
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }
        # updating the trip with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, trip_id)
        if updated is not None:
            return updated
