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
    default: bool

    def __eq__(self, other):
        if isinstance(other, Item):
            return (
                    self.id == other.id and
                    self.name == other.name and
                    self.category == other.category and
                    self.temp_max == other.temp_max and
                    self.temp_min == other.temp_min and
                    self.gender == other.gender and
                    self.default == other.default
            )
        return False

    def __hash__(self):
        return hash((self.id, self.name, self.category, self.temp_max, self.temp_min, self.gender, self.default))
