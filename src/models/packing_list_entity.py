import typing

from pydantic import BaseModel

from src.models import Field, PyObjectId, ConfigDict
from src.models.item_for_trip import ItemForTrip
from typing import List


class PackingListEntity(BaseModel):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    trip_id: str
    items: List[ItemForTrip]
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
