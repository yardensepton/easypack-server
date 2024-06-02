from typing import Optional

from src.models import BaseModel


class City(BaseModel):
    text: str
    place_id: str
    city_name: str
    country_name:  Optional[str] = None
    currency_code: Optional[str] = None
    city_url: Optional[str] = None
