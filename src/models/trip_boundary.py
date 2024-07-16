from typing import Optional
from src.models import ConfigDict
from src.models.trip_update import TripUpdate


class TripBoundary(TripUpdate):
    user_id: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "destination": {
                    "text": "tel aviv, Israel",
                    "place_id": "1234",
                    "city_name": "tel aviv",
                    "country_name": "israel"
                },
                "departure_date": "2025-02-26",
                "return_date": "2025-02-28",
            }
        },
    )
