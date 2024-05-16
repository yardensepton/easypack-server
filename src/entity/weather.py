from src.entity import ConfigDict, BaseModel


class Weather(BaseModel):
    email: str
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
