from datetime import datetime

from fastapi import Depends, HTTPException, status
from jose import JWTError
from jose.jwt import decode

from config import reusable_oauth, JWT_ALGORITHM, JWT_ACCESS_SECRET, JWT_REFRESH_SECRET
from src.models.user_entity import UserEntity
from src.services.user_service import UserService
from src.utils.authantication.password_utils import verify_password_hash
from src.utils.authantication.token_payload import TokenPayload

user_service = UserService()


def decode_token(token: str, secret: str) -> dict:
    try:
        return decode(token, secret, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate user " + str(e),
                            headers={"WWW-Authenticate": "Bearer"})


def validate_token_payload(payload_dict: dict) -> TokenPayload:
    token_payload: TokenPayload = TokenPayload(**payload_dict)
    if datetime.fromisoformat(token_payload.expires) < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired, refresh your token")
    return token_payload


def validate_password(token_payload: TokenPayload) -> UserEntity:
    user: UserEntity = user_service.get_user_by_id(user_id=token_payload.user_id)
    if verify_password_hash(token_payload.user_password, user.password):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password does not match")


def get_current_access_identity(token: str = Depends(reusable_oauth)) -> UserEntity:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in")
    payload_dict = decode_token(token, JWT_ACCESS_SECRET)
    token_payload: TokenPayload = validate_token_payload(payload_dict)
    return validate_password(token_payload)


async def get_current_refresh_identity(token: str = Depends(reusable_oauth)) -> UserEntity:
    payload_dict = decode_token(token, JWT_REFRESH_SECRET)
    token_payload: TokenPayload = validate_token_payload(payload_dict)
    return validate_password(token_payload)
