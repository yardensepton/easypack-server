from typing import Optional

from src.models import Field, PyObjectId
from src.models.user_boundary import UserBoundary


class UserEntity(UserBoundary):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)