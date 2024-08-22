from datetime import timedelta, datetime
from typing import Union

from jose import jwt

from config import *
from src.utils.authantication.token_payload import TokenPayload


def create_access_token(user_id: str, expires_delta: timedelta = None) -> str:

    return token_generator(user_id=user_id, expire_time=ACCESS_TOKEN_EXPIRE_MINUTES, jwt_secret=JWT_ACCESS_SECRET,
                           expires_delta=expires_delta, key="minutes")


def create_refresh_token(user_id: str,  expires_delta: timedelta = None) -> str:
    return token_generator(user_id=user_id, expire_time=REFRESH_TOKEN_EXPIRE_DAYS, jwt_secret=JWT_REFRESH_SECRET,
                           expires_delta=expires_delta, key="days")


def token_generator(user_id: str, expire_time: int, jwt_secret: Union[str, dict],
                    expires_delta: timedelta,
                    key: str) -> str:
    if key == "minutes":
        expires_delta: datetime = datetime.now() + (expires_delta or timedelta(minutes=expire_time))
    elif key == "days":
        expires_delta: datetime = datetime.now() + (expires_delta or timedelta(days=expire_time))
    token_payload: TokenPayload = TokenPayload(expires=expires_delta.isoformat(), user_id=user_id)
    return jwt.encode(token_payload.dict(), jwt_secret, JWT_ALGORITHM)
