from typing import List

from pydantic import BaseModel, ConfigDict

from src.entity.item_boundary import ItemBoundary


class PackingListSchema(BaseModel):
    items: List[ItemBoundary]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "items": []
            }
        },
    )