import re
from pydantic import ConfigDict, field_validator

from src.models.user_schema import UserSchema
from src.enums.role_options import RoleOptions
from src.exceptions.input_error import InputError


class UserBoundary(UserSchema):
    email: str
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

    @field_validator('email')
    @classmethod
    def is_valid_email_format(cls, email: str) -> str:
        email_regex = r"(^[-!#$%&'*+/=?^_`{|}~a-zA-Z0-9]+(\.[-\w]*)*@[-a-zA-Z0-9]+(\.[-\w]*)+\.?[a-zA-Z]{2,}$)"
        if bool(re.match(email_regex, email)) is False:
            raise InputError("Invalid email format")
        return email

    @field_validator('role')
    @classmethod
    def is_valid_role(cls, role: str) -> str:
        if role not in (g.value for g in RoleOptions):
            raise InputError("Invalid role value")
        return role
