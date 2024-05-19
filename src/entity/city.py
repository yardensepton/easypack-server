from src.entity import BaseModel


class City(BaseModel):
    place_id: str
    city_name: str
    city_url: str = None
