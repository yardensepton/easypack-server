from typing import Optional, Annotated, List

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict

from src.entity.item_boundary import ItemBoundary

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
