from datetime import timedelta, datetime
from typing import Union

from jose import jwt

from config import *
from src.utils.authantication.password_utils import get_password_hash
from src.utils.authantication.token_payload import TokenPayload


def create_access_token(user_id: str, user_password: str, expires_delta: timedelta = None) -> str:
    return token_generator(user_id=user_id, expire_time=ACCESS_TOKEN_EXPIRE_MINUTES, jwt_secret=JWT_ACCESS_SECRET,
                           expires_delta=expires_delta, key="minutes",
                           user_password=user_password)


def create_refresh_token(user_id: str, user_password: str, expires_delta: timedelta = None) -> str:
    return token_generator(user_id=user_id, expire_time=ACCESS_TOKEN_EXPIRE_MINUTES, jwt_secret=JWT_ACCESS_SECRET,
                           expires_delta=expires_delta, key="days",
                           user_password=user_password)


def token_generator(user_id: str, user_password: str, expire_time: int, jwt_secret: Union[str, dict],
                    expires_delta: timedelta,
                    key: str) -> str:
    if key == "minutes":
        expires_delta: datetime = datetime.now() + (expires_delta or timedelta(minutes=expire_time))
    elif key == "days":
        expires_delta: datetime = datetime.now() + (expires_delta or timedelta(days=expire_time))
    token_payload: TokenPayload = TokenPayload(expires=expires_delta.isoformat(), user_id=user_id,
                                               user_password=user_password)
    return jwt.encode(token_payload.dict(), jwt_secret, JWT_ALGORITHM)
