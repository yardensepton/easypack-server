from datetime import datetime
from typing import List, Set, Optional

from src.controllers.item_controller import ItemController
from src.controllers.weather_controller import WeatherController
from src.models.item import Item
from src.models.item_for_trip import ItemForTrip
from src.models.packing_list_entity import PackingListEntity
from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.not_found_error import NotFoundError
from db import db
from src.models.packing_list_request import PackingListRequest
from src.models.trip_entity import TripEntity
from src.models.user_entity import UserEntity
from src.repositories.packing_lists_db import PackingListsDB
from src.utils.date_validator import DateValidator


class PackingListService:
    def __init__(self):
        self.db_handler = PackingListsDB(db, "LISTS")
        self.items_controller = ItemController()
        self.weather_controller = WeatherController()

    def get_packing_list_by_id(self, list_id: str) -> PackingListEntity:
        packing_list = self.db_handler.find_one("_id", list_id)
        if packing_list is not None:
            return packing_list
        raise NotFoundError(obj_name="Packing list", obj_id=list_id)

    async def create_packing_list(self, trip: TripEntity, user: UserEntity, lat_lon: dict,
                                  packing_list_request: PackingListRequest) -> PackingListEntity:
        if self.get_packing_list_by_trip_id(trip_id=trip.id):
            raise AlreadyExistsError(obj_name="packing list to trip", obj_id=trip.id)
        packing_list_entity: PackingListEntity = await self.build_packing_list(trip=trip, user=user,
                                                                               lat_lon=lat_lon,
                                                                               packing_list_request=packing_list_request)
        return self.db_handler.insert_one(packing_list_entity)

    async def build_packing_list(self, trip: TripEntity, user: UserEntity, lat_lon: dict,
                                 packing_list_request: PackingListRequest) -> PackingListEntity:
        start_date: datetime = DateValidator.parse_date(trip.departure_date)
        end_date: datetime = DateValidator.parse_date(trip.return_date)
        trip_days: int = (end_date - start_date).days
        print(trip_days)
        trip_days = trip_days if trip_days > 0 else 1
        users_residence_average_temp: int = round(self.weather_controller.get_average_temp_in_user_residence(
            start_date=start_date,
            end_date=end_date, lat_lon=lat_lon))

        average_temp_of_trip: int = round(self.weather_controller.calculate_average_temp(trip.weather_data))
        users_feeling = self.weather_controller.get_user_feeling(average_temp_of_trip=average_temp_of_trip,
                                                                 users_residence_average_temp=users_residence_average_temp)

        print(average_temp_of_trip)
        print(users_feeling)
        print(users_feeling.value)

        all_items: Set[Item] = set()
        packing_list_items: List[ItemForTrip] = []
        # firstly add the basic items based on the user's gender

        basic_items: List[Item] = self.items_controller.filter_items_by(default=True, user_gender=user.gender,
                                                                        user_trip_average_temp=average_temp_of_trip)
        all_items.update(basic_items)

        if packing_list_request.is_work:
            work_items: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                           category="work",
                                                                           user_gender=user.gender)
            all_items.update(work_items)

        # check if it's supposed to rain
        if self.weather_controller.check_if_raining(weather_data=trip.weather_data):
            rain_items: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                           category="rain clothes",
                                                                           user_gender=user.gender)
            all_items.update(rain_items)
        shirts: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                   default=False,
                                                                   category="shirts",
                                                                   user_gender=user.gender)
        print(shirts)

        all_items.update(shirts)
        pants: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                  default=False,
                                                                  category="pants",
                                                                  user_gender=user.gender)
        all_items.update(pants)
        shoes: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                  default=False,
                                                                  category="shoes", user_gender=user.gender)
        all_items.update(shoes)

        mid_layer: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                      default=False,
                                                                      category="mid layer",
                                                                      user_gender=user.gender)
        all_items.update(mid_layer)
        top_layer: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                      default=False,
                                                                      category="top layer",
                                                                      user_gender=user.gender)
        all_items.update(top_layer)

        thermal: List[Item] = self.items_controller.filter_items_by(user_trip_average_temp=average_temp_of_trip,
                                                                    default=False,
                                                                    category="thermal",
                                                                    user_gender=user.gender)
        all_items.update(thermal)

        if packing_list_request.activities_preferences:
            print(packing_list_request.activities_preferences)
            for preference in packing_list_request.activities_preferences:
                print(preference)
                user_preferences: List[Item] = self.items_controller.filter_items_by(category=preference,
                                                                                     user_gender=user.gender,
                                                                                     user_trip_average_temp=average_temp_of_trip)
                all_items.update(user_preferences)

        if packing_list_request.items_preferences:
            for preference in packing_list_request.items_preferences:
                special_item: Item = self.items_controller.get_item_by_name(name=preference)
                all_items.add(special_item)

        for item in all_items:
            item_for_trip: ItemForTrip = self.items_controller.get_item_for_trip(
                item=item,
                trip_days=trip_days
            )
            packing_list_items.append(item_for_trip)
        packing_list_items.sort(key=lambda x: (x.category, x.item_name))
        packing_list_entity: PackingListEntity = PackingListEntity(trip_id=trip.id, items=packing_list_items,
                                                                   description=users_feeling.value,
                                                                   home_average_temp=users_residence_average_temp,
                                                                   trip_average_temp=average_temp_of_trip)

        print(packing_list_entity)
        return packing_list_entity

    def get_packing_list_by_trip_id(self, trip_id: str) -> PackingListEntity:
        packing_list: PackingListEntity = self.db_handler.find_one("trip_id", trip_id)
        if packing_list:
            return packing_list

    def delete_packing_list_by_trip_id(self, trip_id: str) -> None:
        packing_list = self.get_packing_list_by_trip_id(trip_id)
        if packing_list is not None:
            self.db_handler.delete_one("trip_id", trip_id)

    def delete_packing_list_by_id(self, list_id: str) -> None:
        packing_list = self.get_packing_list_by_id(list_id)
        if packing_list is not None:
            self.db_handler.delete_one("_id", list_id)

    def get_all_packing_lists(self) -> List[PackingListEntity]:
        return self.db_handler.find_all()

    async def add_item(self, list_id: str, details: ItemForTrip):
        if self.db_handler.find_one("items.item_name", details.item_name):
            await self.update_item(list_id=list_id, details=details)
        new_info_dict = details.model_dump(by_alias=True, exclude_unset=True)
        self.db_handler.add(new_info=new_info_dict, new_info_name="items",
                            value=list_id)

    async def update_item(self, list_id: str, details: ItemForTrip):
        new_info_dict = details.model_dump(by_alias=True, exclude_unset=True)
        print(new_info_dict)
        self.db_handler.update_specific_field(outer_value=list_id, inner_value=details.item_name,
                                              inner_value_name="item_name",
                                              outer_value_name="items",
                                              update_fields=new_info_dict)

    async def remove_item(self, list_id: str, item_name: str):
        # logging.debug(f"Removing item with id {item_id} from list {list_id}")
        self.db_handler.remove_specific_field(outer_value_name="items", inner_value_name="item_name",
                                              outer_value=list_id, inner_value=item_name)
