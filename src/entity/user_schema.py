from typing import Optional

from src.entity import BaseModel, ConfigDict, field_validator
from src.entity.city import City
from src.enums.gender_options import GenderOptions
from src.exceptions.input_error import InputError


class UserSchema(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
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

    @field_validator('gender')
    @classmethod
    def is_valid_gender(cls, gender: str) -> str:
        if gender not in (g.value for g in GenderOptions):
            raise InputError("Invalid gender value")
        return gender

