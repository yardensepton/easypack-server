from fastapi import HTTPException
from starlette import status

from db import db
from src.repositories import db_handler


class CalculationService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "CALCULATIONS")

    def get_calculations(self, category):
        calculations = self.db_handler.find_one("category",category)
        if calculations:
            return calculations
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"calculations with category {category} not found")
