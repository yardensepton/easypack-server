from src.models.calculation import Calculation
from src.repositories.db_handler import DBHandler


class CalculationsDB(DBHandler):
    def init(self, data: dict) -> Calculation:
        return Calculation(**data)
