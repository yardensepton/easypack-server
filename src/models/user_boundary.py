from pydantic import ConfigDict, field_validator, EmailStr

from src.models.user_schema import UserSchema
from src.enums.role_options import RoleOptions
from src.exceptions.input_error import InputError


class UserBoundary(UserSchema):
    email: EmailStr
    password: str
    role: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jane1@gmail.com",
                "role": "member",
                "gender": "female",
                "password": "123456",
                "city": {
                    "place_id": "112",
                    "text": "San Francisco, California",
                    "city_name": "San Francisco",
                    "country_name": "somewhere"
                }, }
        },
    )

    @field_validator('role')
    @classmethod
    def is_valid_role(cls, role: str) -> str:
        if role not in (g.value for g in RoleOptions):
            raise InputError("Invalid role value")
        return role
