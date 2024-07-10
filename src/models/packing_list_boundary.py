from src.models import BaseModel, ConfigDict, List

from src.models.item_for_trip import ItemForTrip


class PackingListBoundary(BaseModel):
    items: List[ItemForTrip]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "items": []
            }
        },
    )
