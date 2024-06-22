from datetime import datetime, date
from typing import List

from starlette.websockets import WebSocket

from src.controllers.packing_list_controller import PackingListController
from src.models.city import City
from src.models.trip_boundary import TripBoundary
from src.models.trip_entity import TripEntity
from src.models.trip_info import TripInfo
from src.models.trip_schema import TripSchema
from src.models.user_entity import UserEntity
from src.exceptions.input_error import InputError
from src.services.trip_service import TripService


class TripController:

    def __init__(self):
        self.trip_service = TripService()
        self.packing_list_controller = PackingListController()

    def create_trip(self, trip: TripBoundary, user_id: str) -> TripEntity:
        trip_entity: TripEntity = TripEntity(departure_date=trip.departure_date, return_date=trip.return_date,
                                             user_id=user_id, destination=trip.destination)
        departure_date = trip_entity.departure_date
        return_date = trip_entity.return_date
        if self.availability_within_date_range(
                user_id, departure_date, return_date, trip_entity.id):
            return self.trip_service.create_trip(trip=trip_entity)

    def get_trip_by_id(self, trip_id: str) -> TripEntity:
        return self.trip_service.get_trip_by_id(trip_id=trip_id)

    def get_trips_by_user_id(self, user_id: str) -> List[TripEntity]:
        return self.trip_service.get_trips_by_user_id(user_id=user_id)

    def sort_users_trips(self, user_id: str) -> List[TripEntity]:
        trips: List[TripEntity] = self.trip_service.get_trips_by_user_id(user_id=user_id)

        # Parse the departure_date strings into datetime.date objects
        for trip in trips:
            trip.departure_date = datetime.strptime(trip.departure_date, "%Y-%m-%d").date()

        # Filter trips to only include those from today onward
        today = datetime.now().date()
        future_trips = [trip for trip in trips if trip.departure_date >= today]

        # Sort the list by departure_date
        future_trips.sort(key=lambda trip: trip.departure_date)

        # Convert the datetime.date objects back to strings for return
        for trip in future_trips:
            trip.departure_date = trip.departure_date.strftime("%Y-%m-%d")

        return future_trips

    def get_sorted_trips_info(self, user_id: str) -> List[TripInfo]:
        trips: List[TripEntity] = self.sort_users_trips(user_id=user_id)
        trip_info_list: List[TripInfo] = []
        for trip in trips:
            destination: City = trip.destination
            destination_name = destination.name
            trip_info_list.append(
                TripInfo(trip_id=trip.trip_id, departure_date=trip.departure_date, return_date=trip.return_date,
                         destiantion=destination_name))
        return trip_info_list

    def get_users_upcoming_trip(self, user_id: str) -> TripEntity:
        trips: List[TripEntity] = self.sort_users_trips(user_id=user_id)
        return trips[0] if trips else None

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

    def update_trip_by_id(self, new_info: TripSchema, trip_id: str) -> TripEntity:
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
                                          new_info: TripSchema) -> TripEntity:
        if self.are_dates_valid(departure_date, return_date) and self.availability_within_date_range(
                user_id, departure_date, return_date, trip_id):
            return self.trip_service.update_trip_by_id(trip_id=trip_id, new_info=new_info)

    def get_all_trips(self) -> List[TripEntity]:
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
            if trip_id is None or str(trip.id) != trip_id:
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

