from typing import Optional

from pydantic import BaseModel, ConfigDict


class TripUpdate(BaseModel):
    destination:  Optional[str] = None
    departure_date:  Optional[str] = None
    return_date:  Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "destination": "France",
                "departure_date": "2025-04-26",
                "return_date": "2025-04-28",
            }
        },
    )
