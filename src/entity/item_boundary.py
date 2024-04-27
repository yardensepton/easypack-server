from pydantic import BaseModel


class ItemBoundary(BaseModel):
    category: str
    name: str
    amount: float