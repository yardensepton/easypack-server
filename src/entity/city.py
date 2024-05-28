from typing import Optional

from src.entity import BaseModel


class City(BaseModel):
    text: str
    place_id: str
    city_name: str
    country_name: str
    currency_code: Optional[str] = None
    city_url: Optional[str] = None
