import typing

from src.entity import BaseModel, Field, PyObjectId


class Item(BaseModel):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str
    name: str
    gender: str
    season: str
    occasion: str
