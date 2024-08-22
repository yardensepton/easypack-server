from datetime import datetime, timedelta
from typing import List

from src.controllers.packing_list_controller import PackingListController
from src.models.city import City
from src.models.trip_entity import TripEntity
from src.models.trip_info import TripInfo
from src.models.trip_update import TripUpdate
from src.exceptions.input_error import InputError
from src.models.weather import WeatherDay
from src.services.trip_service import TripService
from src.utils.date_validator import DateValidator


class TripController:

    def __init__(self):
        self.trip_service = TripService()
        self.packing_list_controller = PackingListController()

    def create_trip(self, trip_entity: TripEntity) -> TripEntity:
        return self.trip_service.create_trip(trip=trip_entity)

    async def get_trip_by_id(self, trip_id: str) -> TripEntity:
        return await self.trip_service.get_trip_by_id(trip_id=trip_id)

    async def get_trips_by_user_id(self, user_id: str) -> List[TripEntity]:
        return await self.trip_service.get_trips_by_user_id(user_id=user_id)

    async def sort_users_trips(self, user_id: str) -> List[TripEntity]:
        trips: List[TripEntity] = await self.trip_service.get_trips_by_user_id(user_id=user_id)

        # Parse the departure_date strings into datetime.date objects
        for trip in trips:
            trip.departure_date = datetime.strptime(trip.departure_date, "%Y-%m-%d").date()

        # Filter trips to only include those from today onward
        sorted_trips: List[TripEntity] = [trip for trip in trips]

        # Sort the list by departure_date
        sorted_trips.sort(key=lambda trip: trip.departure_date)

        # Convert the datetime.date objects back to strings for return
        for trip in sorted_trips:
            trip.departure_date = trip.departure_date.strftime("%Y-%m-%d")

        return sorted_trips

    async def get_sorted_trips_info(self, user_id: str) -> List[TripInfo]:
        trips: List[TripEntity] = await self.sort_users_trips(user_id=user_id)

        trip_info_list: List[TripInfo] = []
        for trip in trips:
            destination: City = trip.destination
            destination_name = destination.text
            trip_info_list.append(
                TripInfo(trip_id=trip.id, departure_date=trip.departure_date, return_date=trip.return_date,
                         destination=destination_name, city_url=destination.city_url))
        return trip_info_list

    async def get_trips_in_a_week(self, user_id: str) -> List[TripEntity]:
        trips: List[TripEntity] = await self.trip_service.get_trips_by_user_id(user_id=user_id)
        today = datetime.now().date()
        one_week_later = today + timedelta(days=7)

        filtered_trips = []
        for trip in trips:
            trip_date = datetime.strptime(trip.departure_date, "%Y-%m-%d").date()
            if today <= trip_date <= one_week_later:
                trip.departure_date = trip_date  # Store the date as datetime.date
                filtered_trips.append(trip)

        # Sort the filtered trips by departure_date
        filtered_trips.sort(key=lambda checked_trip: checked_trip.departure_date)

        # Convert the datetime.date objects back to strings for return
        for trip in filtered_trips:
            trip.departure_date = trip.departure_date.strftime("%Y-%m-%d")

        return filtered_trips

    async def get_users_upcoming_trip(self, user_id: str) -> TripEntity:
        trips: List[TripEntity] = await self.sort_users_trips(user_id=user_id)
        return trips[0] if trips else None

    def delete_trip_by_id(self, trip_id: str):
        self.trip_service.delete_trip_by_id(trip_id=trip_id)

    async def delete_trips_by_user_id(self, user_id: str):
        trips = await self.get_trips_by_user_id(user_id=user_id)
        if trips is not None:
            for trip_data in trips:
                trip_id = trip_data.id

                if trip_id is not None:
                    self.packing_list_controller.delete_packing_list_by_trip_id(trip_id)
                    self.delete_trip_by_id(trip_id)

    async def update_trip_by_id(self, new_info: TripUpdate, trip_id: str) -> TripEntity:
        """
        Updates a trip by its ID based on the provided new information.

        Args:
            new_info (TripUpdate): The new information for the trip.
            trip_id (str): The ID of the trip to be updated.

        Returns:
            TripEntity: The updated trip entity.
        """
        trip_dict = await self.get_trip_by_id(trip_id)
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
                                          new_info: TripUpdate) -> TripEntity:
        if DateValidator.are_dates_valid(departure_date, return_date) and self.availability_within_date_range(
                user_id, departure_date, return_date, trip_id):
            return self.trip_service.update_trip_by_id(trip_id=trip_id, new_info=new_info)

    def get_all_trips(self) -> List[TripEntity]:
        return self.trip_service.get_all_trips()

    async def availability_within_date_range(self, user_id: str, departure_date: str, return_date: str, trip_id: str) -> bool:
        """
        Checks if a user has any existing trips within the specified date range.

        Args:
            user_id (str): The ID of the user.
            departure_date (str): The departure date of the new trip in "YYYY-MM-DD" format.
            return_date (str): The return date of the new trip in "YYYY-MM-DD" format.
            trip_id (str): The ID of the current trip being checked.

        Returns:
            bool: True if no trip exists within the date range, False otherwise.
        """
        trips = await self.get_trips_by_user_id(user_id=user_id)
        if trips is None:
            return True

        trip_start = DateValidator.parse_date(departure_date)
        trip_end = DateValidator.parse_date(return_date)

        # Retrieve all trips associated with the user from the database

        # Iterate through the list of trips
        for trip in trips:
            if trip_id is None or str(trip.id) != trip_id:
                current_trip_start = DateValidator.parse_date(trip.departure_date)
                current_trip_end = DateValidator.parse_date(trip.return_date)

                # Check if the trip falls within the specified date range
                if trip_start <= current_trip_start <= trip_end or trip_start <= current_trip_end <= trip_end:
                    raise InputError(f"User '{user_id}' has a trip within the date range")

        # No trip found within the date range
        return True

    def update_trip_weather_data(self, trip: TripEntity, new_weather_data: List[WeatherDay]):
        self.trip_service.update_trip_weather_data(new_weather_data=new_weather_data, trip_id=trip.id)
