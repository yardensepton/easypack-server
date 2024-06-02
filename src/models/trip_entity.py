import typing

from pydantic import Field

from src.models import PyObjectId
from src.models.trip_boundary import TripBoundary


class TripEntity(TripBoundary):
    id: typing.Optional[PyObjectId] = Field(alias="_id", default=None)
