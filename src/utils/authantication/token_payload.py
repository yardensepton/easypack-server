from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: str
    user_password: str
    expires: str
