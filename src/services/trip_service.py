from typing import List

from logger import logger
from src.models.trip_entity import TripEntity
from src.models.trip_update import TripUpdate
from src.exceptions.not_found_error import NotFoundError
from db import db
from src.models.weather import WeatherDay
from src.repositories.trips_db import TripsDB


class TripService:

    def __init__(self):
        self.db_handler = TripsDB(db, "TRIPS")
        self.logger = logger

    def create_trip(self, trip: TripEntity) -> TripEntity:
        """
        Create a new trip and store it in the database.

        Args:
            trip (TripEntity): The trip details to be added.

        Returns:
            TripEntity: The created trip entity.

        Logs:
            Info message indicating that the trip was added successfully.
        """

        trip_in_db: TripEntity = self.db_handler.insert_one(trip)
        self.logger.info(f"Trip {trip_in_db.id} was added successfully")
        return trip_in_db

    async def get_trip_by_id(self, trip_id: str) -> TripEntity:
        """
                Retrieve a trip from the database by its ID.

                Args:
                    trip_id (str): The ID of the trip to retrieve.

                Returns:
                    TripEntity: The trip entity if found.

                Raises:
                    NotFoundError: If no trip is found with the given ID.
                """
        trip = self.db_handler.find_one("_id", trip_id)
        if trip is not None:
            return trip
        raise NotFoundError(obj_name="Trip", obj_id=trip_id)

    async def get_trips_by_user_id(self, user_id: str) -> List[TripEntity]:
        """
               Retrieve all trips associated with a specific user ID.

               Args:
                   user_id (str): The ID of the user whose trips are to be retrieved.

               Returns:
                   List[TripEntity]: A list of trips for the specified user.
               """
        return self.db_handler.find({"user_id": user_id})

    def delete_trips_by_user_id(self, user_id: str):
        """
               Delete all trips associated with a specific user ID.

               Args:
                   user_id (str): The ID of the user whose trips are to be deleted.

               Returns:
                   None

               Logs:
                   Info message indicating that the trips for the user were deleted.
               """
        trips = self.get_trips_by_user_id(user_id)
        if trips is not None:
            self.logger.info(f"Trips of {user_id} were deleted successfully")
            self.db_handler.delete_many({"user_id": user_id})

    async def delete_trip_by_id(self, trip_id):
        """
               Delete a trip from the database by its ID.

               Args:
                   trip_id (str): The ID of the trip to delete.

               Returns:
                   None

               Logs:
                   Info message indicating that the trip was deleted.
               """
        trip = await self.get_trip_by_id(trip_id)
        if trip is not None:
            self.logger.info(f"Trip {trip_id} was deleted successfully")
            self.db_handler.delete_one("_id", trip_id)

    def update_trip_by_id(self, new_info: TripUpdate, trip_id: str) -> TripEntity:
        """
               Update the details of the trip in the database.

               Args:
                   new_info (TripUpdate): The new information to update.
                   trip_id (str): The ID of the trip to update.

               Returns:
                   TripEntity: The updated trip entity.

               Raises:
                   NotFoundError: If no trip is found with the given ID.

               Logs:
                   Info message indicating that the trip was updated successfully.
               """
        # adding the input values to a dict if they are not null
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }
        # updating the trip with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, trip_id)

        if updated is not None:
            self.logger.info(f"Trip {trip_id} was updated successfully")
            return updated
        raise NotFoundError(obj_name="trip", obj_id=trip_id)

    def get_all_trips(self) -> List[TripEntity]:
        """
                Retrieve all trips from the database.

                Returns:
                    List[TripEntity]: A list of all trip entities.
                """
        return self.db_handler.find_all()

    def update_trip_weather_data(self, new_weather_data: List[WeatherDay], trip_id: str) -> TripEntity:
        """
               Update the weather data for a specific trip.

               Args:
                   new_weather_data (List[WeatherDay]): A list of new weather data to update.
                   trip_id (str): The ID of the trip to update.

               Returns:
                   TripEntity: The updated trip entity with new weather data.

               Raises:
                   NotFoundError: If no trip is found with the given ID.
               """
        weather_data_dicts = [weather_day.to_dict() for weather_day in new_weather_data]
        updated = self.db_handler.find_one_and_update({"weather_data": weather_data_dicts}, trip_id)
        if updated is not None:
            self.logger.info(f"Trip {trip_id}'s weather was updated successfully")
            return updated
        raise NotFoundError(obj_name="trip", obj_id=trip_id)
