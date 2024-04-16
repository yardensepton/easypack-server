from db import db
from src.exceptions.calculation_not_found_error import CalculationNotFoundError
from src.repositories import db_handler


class CalculationService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "CALCULATIONS")

    def get_calculations(self, category):
        calculations = self.db_handler.find_one("category",category)
        if calculations:
            return calculations
        raise CalculationNotFoundError(category)
