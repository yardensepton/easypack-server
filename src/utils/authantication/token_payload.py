from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: str
    expires: str
