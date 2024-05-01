from pymongo.collection import Collection, ReturnDocument
from pymongo.cursor import Cursor
from pymongo.database import Database
from typing import Any, List
from bson import ObjectId

from src.repositories.db_handler_base import DBHandlerBase


class DBHandler(DBHandlerBase):

    def __init__(self, db: Database, collection_name):
        self.collection: Collection = db[collection_name]

    def exists(self, key: str, value: str) -> Any:
        return self.collection.count_documents({key: value}) > 0

    def delete_many(self, keys_and_values: dict[str, str]) -> Any:
        return self.collection.delete_many(keys_and_values)

    def insert_one(self, value: Any) -> Any:
        new_object = self.collection.insert_one(value.model_dump(by_alias=True, exclude=["id"]))
        created_object = self.collection.find_one(
            {"_id": new_object.inserted_id}
        )
        return created_object

    def find_one(self, key: str, value: str) -> Any:
        value = self.add_object_id(key, value)
        return self.collection.find_one({key: value})

    def delete_one(self, key: str, value: str) -> Any:
        value = self.add_object_id(key, value)
        return self.collection.delete_one({key: value})

    def find(self, keys_and_values: dict[str, any]) -> List[Any]:
        cursor: Cursor = self.collection.find(keys_and_values)
        return list(cursor)

    def find_all(self) -> List[Any]:
        cursor: Cursor = self.collection.find()
        return list(cursor)

    def find_one_and_update(self, new_info: Any, key: str) -> Any:
        if len(new_info) >= 1:
            update_result = self.collection.find_one_and_update(
                {"_id": ObjectId(key)},
                {"$set": new_info},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return update_result

            else:
                return None

    def add_object_id(self, key: str, value: str) -> str:
        if key == '_id':
            value = ObjectId(value)
        return value
