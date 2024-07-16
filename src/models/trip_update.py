from typing import Optional, Self

from src.models import BaseModel, ConfigDict, model_validator
from src.models.city import City

from src.exceptions.input_error import InputError
from src.utils.date_validator import DateValidator


class TripUpdate(BaseModel):
    destination: Optional[City] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "destination": {
                    "text": "tel aviv, Israel",
                    "place_id": "1234",
                    "city_name": "tel aviv"
                },
                "departure_date": "2025-04-26",
                "return_date": "2025-04-28",
            }
        },
    )

    @model_validator(mode='after')
    def check_valid_dates(self) -> Self:
        if self.departure_date and self.return_date:
            date1 = DateValidator.parse_date(self.departure_date)
            date2 = DateValidator.parse_date(self.return_date)
            if date1 > date2:
                raise InputError("Return date is before departure date")
            return self
        return self

