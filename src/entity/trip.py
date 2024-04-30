from typing import Optional, Annotated
from pydantic import Field, ConfigDict, BeforeValidator

from src.entity.trip_schema import TripSchema


PyObjectId = Annotated[str, BeforeValidator(str)]


class Trip(TripSchema):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "your_user_id_value",
                "destination": "London",
                "departure_date": "2025-02-26",
                "return_date": "2025-02-28",
            }
        },
    )

