from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from src.enums.gender_options import GenderOptions
from src.exceptions.input_error import InputError


class UserSchema(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    residence: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "gender": "female",
                "residence": "Israel",
            }
        },
    )

    @field_validator('gender')
    @classmethod
    def is_valid_gender(cls, gender: str) -> str:
        if gender not in (g.value for g in GenderOptions):
            raise InputError("Invalid gender value")
        return gender
