from datetime import datetime

from fastapi import Depends, HTTPException, status
from jose import JWTError
from jose.jwt import decode

from config import reusable_oauth, JWT_ALGORITHM, JWT_ACCESS_SECRET, JWT_REFRESH_SECRET
from src.models.user_entity import UserEntity
from src.services.user_service import UserService
from src.utils.authantication.token_payload import TokenPayload

user_service = UserService()


def decode_token(token: str, secret: str) -> dict:
    """
    Decode a JWT token using the provided secret.

    Args:
        token (str): The JWT token to decode.
        secret (str): The secret key to validate the token.

    Returns:
        dict: The decoded token payload.

    Raises:
        HTTPException: If the token cannot be decoded or is invalid.
    """
    try:
        return decode(token, secret, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate user " + str(e),
                            headers={"WWW-Authenticate": "Bearer"})


def validate_token_payload(payload_dict: dict) -> TokenPayload:
    """
       Validate the token payload and check if the token has expired.

       Args:
           payload_dict (dict): The token payload to validate.

       Returns:
           TokenPayload: The validated token payload.

       Raises:
           HTTPException: If the token is expired.
       """
    token_payload: TokenPayload = TokenPayload(**payload_dict)
    if datetime.fromisoformat(token_payload.expires) < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired, refresh your token")
    return token_payload


async def get_current_access_identity(token: str = Depends(reusable_oauth)) -> UserEntity:
    """
       Get the current user identity from the access token.

       Args:
           token (str): The access token.

       Returns:
           UserEntity: The user entity associated with the access token.

       Raises:
           HTTPException: If the token is missing, invalid, or the user cannot be found.
       """
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in")
    payload_dict = decode_token(token, JWT_ACCESS_SECRET)
    token_payload: TokenPayload = validate_token_payload(payload_dict)
    return await user_service.get_user_by_id(user_id=token_payload.user_id)


async def get_current_refresh_identity(token: str = Depends(reusable_oauth)) -> UserEntity:
    """
       Get the current user identity from the refresh token.

       Args:
           token (str): The refresh token.

       Returns:
           UserEntity: The user entity associated with the refresh token.

       Raises:
           HTTPException: If the token is invalid or the user cannot be found.
       """
    payload_dict = decode_token(token, JWT_REFRESH_SECRET)
    token_payload: TokenPayload = validate_token_payload(payload_dict)
    return await user_service.get_user_by_id(user_id=token_payload.user_id)
