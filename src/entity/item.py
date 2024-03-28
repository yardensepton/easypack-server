from typing import Optional, Annotated

from pydantic import BaseModel, Field, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class Item(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str
    name: str
    gender: str
    season: str
    occasion: str
