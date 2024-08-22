from typing import Optional

from src.models import BaseModel, ConfigDict
from src.models.city import City
from src.enums.gender_options import GenderOptions


class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[GenderOptions] = None
    city: Optional[City] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "gender": "female",
                "city": {
                    "place_id": "112",
                    "text":"San Francisco, California",
                    "city_name": "San Francisco",
                    "country_name": "somewhere"
                },
            }
        },
    )

