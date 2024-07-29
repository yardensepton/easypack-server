from typing import Optional

from pydantic import BaseModel


class ItemForTrip(BaseModel):
    item_name: str
    category: str
    amount_per_trip: int
    is_packed: Optional[bool] = False
