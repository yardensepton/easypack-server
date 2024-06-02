import typing

from src.models import Field, PyObjectId
from src.models.user_boundary import UserBoundary


class UserEntity(UserBoundary):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)