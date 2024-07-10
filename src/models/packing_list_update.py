from pydantic import BaseModel

from src.enums.operation import Operation
from src.models.item_for_trip import ItemForTrip


class PackingListUpdate(BaseModel):
    operation: Operation
    details: ItemForTrip
