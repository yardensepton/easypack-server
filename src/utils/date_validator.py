from datetime import datetime

from src.exceptions.input_error import InputError


class DateValidator:
    @staticmethod
    def parse_date(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as ve:
            raise ValueError(f"invalid date: {ve}")

    @staticmethod
    def are_dates_valid(departure_date: str, return_date: str) -> bool:
        # check if the return date is before the departure date
        if departure_date and return_date:
            date1 = DateValidator.parse_date(departure_date)
            date2 = DateValidator.parse_date(return_date)
            if date1 > date2:
                raise InputError("Return date is before departure date")
        return True
