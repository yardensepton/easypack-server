from typing import Optional, Annotated

from bson import ObjectId
from pydantic import Field, ConfigDict, BeforeValidator, field_validator

from src.entity.trip_schema import TripSchema
from src.exceptions.input_error import InputError

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


    @field_validator('user_id')
    @classmethod
    def is_valid_user_id(cls, user_id: str) -> str:
        if user_id is not None:
            try:
                ObjectId(user_id)
            except Exception:
                raise InputError(f"'{user_id}' is not a valid ObjectId")
        return user_id