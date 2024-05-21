from src.entity import BaseModel


class City(BaseModel):
    text:str
    place_id: str
    city_name: str
    city_url: str = None
