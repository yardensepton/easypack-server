from functools import wraps

from fastapi import HTTPException, status

from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.models.trip_boundary import TripBoundary
from src.enums.role_options import RoleOptions

trip_controller = TripController()
packing_list_controller = PackingListController()


def user_trip_obj_access_or_abort(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        trip: TripBoundary = kwargs.get('trip')
        identity = kwargs.get('identity')
        if identity.role == RoleOptions.ADMIN.value:
            return await func(*args, **kwargs)
        if trip.user_id != identity.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return await func(*args, **kwargs)

    return wrapper


def user_trip_access_or_abort(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        trip_id = kwargs.get('trip_id')
        identity = kwargs.get('identity')
        trip: TripBoundary = await trip_controller.get_trip_by_id(trip_id)
        if identity.role == RoleOptions.ADMIN.value:
            return await func(*args, **kwargs)
        if trip.user_id != identity.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return await func(*args, **kwargs)

    return wrapper
