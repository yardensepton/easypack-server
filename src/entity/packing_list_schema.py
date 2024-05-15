from src.entity import BaseModel, ConfigDict, List

from src.entity.item_and_calculation import ItemAndCalculation


class PackingListSchema(BaseModel):
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
