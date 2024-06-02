import typing

from src.models import Field, PyObjectId, ConfigDict
from src.models.packing_list_boundary import PackingListBoundary


class PackingListEntity(PackingListBoundary):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    trip_id: str
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
