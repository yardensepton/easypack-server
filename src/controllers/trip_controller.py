from datetime import datetime
from typing import List
from src.controllers.packing_list_controller import PackingListController
from src.entity.trip import Trip
from src.entity.trip_schema import TripSchema
from src.exceptions.input_error import InputError
from src.services.trip_service import TripService


class TripController:

    def __init__(self):
        self.trip_service = TripService()
        self.packing_list_controller = PackingListController()

    def create_trip(self, trip: Trip) -> Trip:
        user_id = trip.user_id
        departure_date = trip.departure_date
        return_date = trip.return_date
        if self.availability_within_date_range(
                user_id, departure_date, return_date, trip.id):
            return self.trip_service.create_trip(trip=trip)

    def get_trip_by_id(self, trip_id: str) -> Trip:
        return self.trip_service.get_trip_by_id(trip_id=trip_id)

    def get_trips_by_user_id(self, user_id: str) -> List[Trip]:
        return self.trip_service.get_trips_by_user_id(user_id=user_id)

    def delete_trip_by_id(self, trip_id: str):
        self.trip_service.delete_trip_by_id(trip_id=trip_id)

    def delete_trips_by_user_id(self, user_id: str):
        trips = self.get_trips_by_user_id(user_id=user_id)
        if trips is not None:
            for trip_data in trips:
                trip_id = trip_data.id

                if trip_id is not None:
                    self.packing_list_controller.delete_packing_list_by_trip_id(trip_id)
                    self.delete_trip_by_id(trip_id)

    def update_trip_by_id(self, new_info: TripSchema, trip_id: str) -> Trip:
        trip_dict = self.get_trip_by_id(trip_id)
        if trip_dict is not None:
            user_id = trip_dict.user_id

            # both of the dates were given
            if new_info.departure_date and new_info.return_date:
                return self.check_departure_and_return_inputs(user_id, new_info.departure_date, new_info.return_date,
                                                              trip_id,
                                                              new_info)
            # only departure_date was given
            elif new_info.departure_date and not new_info.return_date:
                return self.check_departure_and_return_inputs(user_id, new_info.departure_date, trip_dict.return_date,
                                                              trip_id,
                                                              new_info)
            # only return_date was given
            elif new_info.return_date and not new_info.departure_date:
                return self.check_departure_and_return_inputs(user_id, trip_dict.departure_date, new_info.return_date,
                                                              trip_id,
                                                              new_info)
            # only destination was given
            elif new_info.destination:
                return self.trip_service.update_trip_by_id(trip_id=trip_id, new_info=new_info)

    def check_departure_and_return_inputs(self, user_id: str, departure_date: str, return_date: str, trip_id: str,
                                          new_info: TripSchema) -> Trip:
        if self.are_dates_valid(departure_date, return_date) and self.availability_within_date_range(
                user_id, departure_date, return_date, trip_id):
            return self.trip_service.update_trip_by_id(trip_id=trip_id, new_info=new_info)

    def get_all_trips(self) -> List[Trip]:
        return self.trip_service.get_all_trips()

    def availability_within_date_range(self, user_id: str, departure_date: str, return_date: str, trip_id: str) -> bool:
        # check if the user already has a trip within the given date range
        trips = self.get_trips_by_user_id(user_id=user_id)
        if trips is None:
            return True

        trip_start = self.parse_date(departure_date)
        trip_end = self.parse_date(return_date)

        # Retrieve all trips associated with the user from the database

        # Iterate through the list of trips
        for trip in trips:
            # trip = Trip(**trip)
            if str(trip.id) != trip_id:
                current_trip_start = self.parse_date(trip.departure_date)
                current_trip_end = self.parse_date(trip.return_date)

                # Check if the trip falls within the specified date range
                if trip_start <= current_trip_start <= trip_end or trip_start <= current_trip_end <= trip_end:
                    raise InputError(f"User '{user_id}' has a trip within the date range")

        # No trip found within the date range
        return True

    def parse_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as ve:
            raise ValueError(f"invalid date: {ve}")

    def are_dates_valid(self, departure_date: str, return_date: str) -> bool:
        # check if the return date is before the departure date
        if departure_date and return_date:
            date1 = self.parse_date(departure_date)
            date2 = self.parse_date(return_date)
            if date1 > date2:
                raise InputError("Return date is before departure date")
        return True
