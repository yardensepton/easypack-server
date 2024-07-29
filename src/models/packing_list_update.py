from pydantic import BaseModel

from src.enums.action import Action
from src.models.item_for_trip import ItemForTrip


class PackingListUpdate(BaseModel):
    action: Action
    details: ItemForTrip
