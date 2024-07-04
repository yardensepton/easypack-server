from datetime import datetime


class DateValidator:
    @staticmethod
    def parse_date(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as ve:
            raise ValueError(f"invalid date: {ve}")
