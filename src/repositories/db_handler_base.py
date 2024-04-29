from abc import ABC, abstractmethod
from typing import Any, List


class DBHandlerBase(ABC):

    @abstractmethod
    def insert_one(self, value: Any) -> Any:
        pass

    @abstractmethod
    def find_one(self, key: str, value: str) -> Any:
        pass

    @abstractmethod
    def delete_one(self, key: str, value: str) -> Any:
        pass

    @abstractmethod
    def delete_many(self, keys_and_values: dict[str, str]) -> Any:
        pass

    @abstractmethod
    def find(self, keys_and_values: dict[str, str]) -> List[Any]:
        pass

    @abstractmethod
    def find_all(self) -> List[Any]:
        pass

    @abstractmethod
    def find_one_and_update(self, new_info:Any, key:str) -> Any:
        pass

    @abstractmethod
    def exists(self, key: str, value: str) -> Any:
        pass

    # @abstractmethod
    # def update_object_by(self, value: Any) -> Any:
    #     pass
    #
    # def delete_object_by(self, key: str, value: str) -> Any:
    #     pass
    #
    # def get_all_objects_by(self, key: str, value: str) -> List[Any]:
    #     pass
