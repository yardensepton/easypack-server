from pydantic import BaseModel

from src.entity.item_and_calculation import ItemAndCalculation
from src.enums.operation import Operation


class PackingListUpdate(BaseModel):
    operation: Operation
    details: ItemAndCalculation
