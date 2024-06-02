from src.models.user_entity import UserEntity
from src.repositories.db_handler import DBHandler


class UsersDB(DBHandler):
    def init(self, data: dict) -> UserEntity:
        return UserEntity(**data)
