import typing
from typing import Optional
from src.models import BaseModel, Field, PyObjectId


class Item(BaseModel):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str
    name: str
    gender: str
    temp_max: Optional[int] = None
    temp_min: Optional[int] = None
