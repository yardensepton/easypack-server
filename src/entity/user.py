import typing

from src.entity import Field, PyObjectId, ConfigDict, field_validator
from src.entity.user_schema import UserSchema
import re
from src.exceptions.input_error import InputError


class User(UserSchema):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jane@gmail.com",
                "gender": "female",
                "city": {
                    "place_id": "112",
                    "text": "San Francisco, California",
                    "city_name": "San Francisco",
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
