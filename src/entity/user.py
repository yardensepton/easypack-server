from typing import Annotated, Optional
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict, field_validator
import re
from src.exceptions.input_error import InputError

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: str
    gender: str
    residence: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jane@gmail.com",
                "gender": "female",
                "residence": "Israel"}
        },
    )

    @field_validator('email')
    @classmethod
    def is_valid_email_format(cls, email: str) -> str:
        email_regex = r"(^[-!#$%&'*+/=?^_`{|}~a-zA-Z0-9]+(\.[-\w]*)*@[-a-zA-Z0-9]+(\.[-\w]*)+\.?[a-zA-Z]{2,}$)"
        if bool(re.match(email_regex, email)) is False:
            raise InputError("Invalid email format")
        return email
