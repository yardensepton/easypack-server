import typing

from src.models import Field, PyObjectId, ConfigDict
from src.models.trip_schema import TripSchema


class TripBoundary(TripSchema):
    # id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "your_user_id_value",
                "destination": {
                    "text": "tel aviv, Israel",
                    "place_id": "1234",
                    "city_name": "tel aviv",
                    "country_name":"israel"
                },
                "departure_date": "2025-02-26",
                "return_date": "2025-02-28",
            }
        },
    )
