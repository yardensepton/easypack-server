from src.entity.user import User
from src.repositories.db_handler import DBHandler


class UsersDB(DBHandler):
    def init(self, data: dict) -> User:
        return User(**data)
