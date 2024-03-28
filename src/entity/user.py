from typing import Annotated, Optional
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict

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
                "residence": "Israel"            }
        },
    )
