from pydantic import ConfigDict, EmailStr

from src.models.user_update import UserUpdate
from src.enums.role_options import RoleOptions


class UserBoundary(UserUpdate):
    email: EmailStr
    password: str
    role: RoleOptions
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