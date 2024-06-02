from functools import wraps

from fastapi import HTTPException, status

from src.models.user_entity import UserEntity
from src.enums.role_options import RoleOptions


def user_permission_check(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user_id: str = kwargs.get('user_id')
        identity: UserEntity = kwargs.get('identity')
        if identity.role == RoleOptions.ADMIN.value:
            return await func(*args, **kwargs)

        if user_id != identity.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return await func(*args, **kwargs)

    return wrapper

