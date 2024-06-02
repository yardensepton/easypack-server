import typing

from src.models import BaseModel, Field, PyObjectId


class Calculation(BaseModel):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str
    amountPerDay: float
