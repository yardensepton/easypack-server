from db import db
from src.exceptions.not_found_error import NotFoundError
from src.repositories import db_handler


class CalculationService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "CALCULATIONS")

    def get_calculations(self, category:str):
        calculations = self.db_handler.find_one("category",category)
        if calculations:
            return calculations
        raise NotFoundError(obj_name="Calculation under the category", obj_id=category)
