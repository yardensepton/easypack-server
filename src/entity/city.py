from typing import Optional

from src.entity import BaseModel


class City(BaseModel):
    text:str
    place_id: str
    city_name: str
    city_url: Optional[str] = None
