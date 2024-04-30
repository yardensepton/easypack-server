from typing import Optional, Annotated, Dict, List

from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict, field_validator

from src.entity.item_boundary import ItemBoundary
from src.exceptions.input_error import InputError

PyObjectId = Annotated[str, BeforeValidator(str)]


class PackingList(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    trip_id: str
    items: List[ItemBoundary]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "trip_id": "your_trip_id_value",
                "items": []
            }
        },
    )

    @field_validator('trip_id')
    @classmethod
    def is_valid_trip_id(cls, trip_id: str) -> str:
        if trip_id is not None:
            try:
                ObjectId(trip_id)
            except Exception:
                raise InputError(f"'{trip_id}' is not a valid ObjectId")
        return trip_id

