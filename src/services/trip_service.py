import asyncio
from typing import List

from bson import json_util
import json
from pymongo.errors import PyMongoError
from starlette.websockets import WebSocket, WebSocketDisconnect
from watchfiles import Change

from src.models.trip_entity import TripEntity
from src.models.trip_schema import TripSchema
from src.exceptions.not_found_error import NotFoundError
from db import db
from src.repositories.trips_db import TripsDB


class TripService:

    def __init__(self):
        self.db_handler = TripsDB(db, "TRIPS")
        self.active_connections: List[WebSocket] = []

    def create_trip(self, trip: TripEntity) -> TripEntity:
        return self.db_handler.insert_one(trip)

    def get_trip_by_id(self, trip_id: str) -> TripEntity:
        trip = self.db_handler.find_one("_id", trip_id)
        if trip is not None:
            return trip
        raise NotFoundError(obj_name="Trip", obj_id=trip_id)

    def get_trips_by_user_id(self, user_id: str) -> List[TripEntity]:
        return self.db_handler.find({"user_id": user_id})

    def delete_trips_by_user_id(self, user_id: str):
        trips = self.get_trips_by_user_id(user_id)
        if trips is not None:
            self.db_handler.delete_many({"user_id": user_id})

    def delete_trip_by_id(self, trip_id):
        trip = self.get_trip_by_id(trip_id)
        if trip is not None:
            self.db_handler.delete_one("_id", trip_id)

    def update_trip_by_id(self, new_info: TripSchema, trip_id: str) -> TripEntity:
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

    # async def listen_to_changes_in_db(self, websocket: WebSocket):
    #     self.active_connections.append(websocket)
    #     pipeline = [
    #         {
    #             '$match': {
    #                 'operationType': {'$in': ['insert', 'delete']},
    #                 # 'fullDocument.user_id': user_id  # Assuming user_id field in the document
    #             }
    #         }
    #     ]
    #
    #     stream = self.db_handler.watch(pipeline)
    #
    #     try:
    #         while True:
    #             try:
    #                 change = await asyncio.to_thread(stream.next)
    #                 if change:
    #                     # Convert change to JSON serializable format
    #                     # Notify connected WebSocket clients about the change
    #                     await websocket.send_text("update in db")
    #             except WebSocketDisconnect:
    #                 break
    #             except PyMongoError as e:
    #                 print(f"Error in change stream: {e}")
    #                 break
    #     finally:
    #         self.active_connections.remove(websocket)
    #         await websocket.close()
    #         stream.close()
