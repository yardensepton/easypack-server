from datetime import datetime

from src.exceptions.input_error import InputError


class DateValidator:
    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """
               Parse a date string into a datetime object.

               Args:
                   date_str (str): The date string in the format "%Y-%m-%d".

               Returns:
                   datetime: The parsed datetime object.

               Raises:
                   ValueError: If the date string is invalid or does not match the expected format.
               """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as ve:
            raise ValueError(f"invalid date: {ve}")

    @staticmethod
    def are_dates_valid(departure_date: str, return_date: str) -> bool:
        """
               Validate that the departure date is before the return date.

               Args:
                   departure_date (str): The departure date in the format "%Y-%m-%d".
                   return_date (str): The return date in the format "%Y-%m-%d".

               Returns:
                   bool: True if the dates are valid, otherwise raises an InputError.

               Raises:
                   InputError: If the return date is before the departure date.
               """
        if departure_date and return_date:
            date1 = DateValidator.parse_date(departure_date)
            date2 = DateValidator.parse_date(return_date)
            if date1 > date2:
                raise InputError("Return date is before departure date")
        return True
