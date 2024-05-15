from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from src.repositories import T


class DBHandlerBase(ABC):

    @abstractmethod
    def insert_one(self, value: T) -> T:
        pass

    @abstractmethod
    def find_one(self, key: str, value: str) -> T:
        pass

    @abstractmethod
    def delete_one(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def delete_many(self, keys_and_values: dict[str, str]) -> None:
        pass

    @abstractmethod
    def find(self, keys_and_values: dict[str, str]) -> List[T]:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def find_one_and_update(self, new_info: Dict, key: str) -> Optional[T]:
        pass

    @abstractmethod
    def exists(self, key: str, value: str) -> bool:
        pass

