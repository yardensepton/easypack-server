from abc import abstractmethod

from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from typing import List, Dict, Optional
from bson import ObjectId

from src.repositories.db_handler_base import DBHandlerBase
from src.repositories import T


class DBHandler(DBHandlerBase):

    def __init__(self, db: Database, collection_name):
        self.collection: Collection = db[collection_name]

    @abstractmethod
    def init(self, data: dict) -> T:
        pass

    def exists(self, key: str, value: str) -> bool:
        return self.collection.count_documents({key: value}) > 0

    def delete_many(self, keys_and_values: dict[str, str]) -> None:
        self.collection.delete_many(keys_and_values)

    def insert_one(self, value: T) -> T:
        new_object = self.collection.insert_one(value.model_dump(by_alias=True, exclude='_id'))
        created_object = self.collection.find_one(
            {"_id": new_object.inserted_id}
        )
        return self.init(created_object)

    def find_one(self, key: str, value: str) -> T:
        value = self.add_object_id(key, value)
        obj: Dict = self.collection.find_one({key: value})
        if obj:
            return self.init(obj)

    def delete_one(self, key: str, value: str) -> None:
        value = self.add_object_id(key, value)
        self.collection.delete_one({key: value})

    def find(self, keys_and_values: dict[str, str]) -> List[T]:
        return [self.init(obj) for obj in self.collection.find(keys_and_values)]

    def find_all(self) -> List[T]:
        return [self.init(obj) for obj in self.collection.find()]

    def find_one_and_update(self, new_info: Dict, key: str) -> Optional[T]:
        if len(new_info) >= 1:
            updated_obj: Dict = self.collection.find_one_and_update(
                {"_id": ObjectId(key)},
                {"$set": new_info},
                return_document=ReturnDocument.AFTER,
            )

            if updated_obj is not None:
                return self.init(updated_obj)

        return None

    def add(self, new_info_name: str, new_info: Dict, value: str) -> Optional[T]:
        updated: Dict = self.collection.find_one_and_update(
            {"_id": ObjectId(value)},
            {"$addToSet": {new_info_name: new_info}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        # Initialize the updated object if found
        if updated is not None:
            return self.init(updated)

        return None

    def update_specific_field(self, outer_value: str, inner_value: str, outer_value_name: str, inner_value_name: str,
                              update_fields: Dict) -> Optional[T]:
        object_id = self.add_object_id("_id", outer_value)
        updated_obj: Dict = self.collection.find_one_and_update(
            {"_id": object_id, f"{outer_value_name}.{inner_value_name}": inner_value},
            {"$set": {f"{outer_value_name}.$.{k}": v for k, v in update_fields.items()}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        if updated_obj is not None:
            return self.init(updated_obj)
        return None

    def remove_specific_field(self, outer_value: str, outer_value_name: str, inner_value: str, inner_value_name: str) -> \
            Optional[Dict]:
        object_id = self.add_object_id("_id", outer_value)
        query = {"_id": object_id}
        update = {"$pull": {outer_value_name: {inner_value_name: inner_value}}}
        updated_obj: Dict = self.collection.find_one_and_update(
            query,
            update,
            return_document=ReturnDocument.AFTER
        )
        if updated_obj is not None:
            return self.init(updated_obj)
        return None

    @classmethod
    def add_object_id(cls, key: str, value: str) -> str:
        if key == '_id':
            value = ObjectId(value)
        return value
