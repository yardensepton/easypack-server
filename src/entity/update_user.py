from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserUpdate(BaseModel):
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
