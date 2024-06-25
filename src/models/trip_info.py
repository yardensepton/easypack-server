from pydantic import BaseModel


class TripInfo(BaseModel):
    trip_id: str
    destination: str
    departure_date: str
    return_date: str
    city_url: str
