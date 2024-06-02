from src.models import BaseModel, ConfigDict, List

from src.models.item_and_calculation import ItemAndCalculation


class PackingListBoundary(BaseModel):
    items: List[ItemAndCalculation]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "items": []
            }
        },
    )
