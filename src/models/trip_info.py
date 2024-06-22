from pydantic import BaseModel


class TripInfo(BaseModel):
    trip_id: int
    destination: str
    departure_date: str
    return_date: str
