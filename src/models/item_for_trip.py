from pydantic import BaseModel


class ItemForTrip(BaseModel):
    item_name: str
    category: str
    amount_per_trip: int
