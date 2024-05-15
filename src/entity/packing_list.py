import typing

from src.entity import BaseModel, Field, PyObjectId, ConfigDict
from src.entity.item_and_calculation import ItemAndCalculation


class PackingList(BaseModel):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    trip_id: str
    items: typing.List[ItemAndCalculation]
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
