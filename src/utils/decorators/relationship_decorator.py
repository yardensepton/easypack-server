from functools import wraps

from fastapi import HTTPException, status

from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.models.trip_boundary import TripBoundary
from src.enums.role_options import RoleOptions

trip_controller = TripController()
packing_list_controller = PackingListController()


def user_trip_obj_access_or_abort(func):
    """
       Decorator to check if the user has access to a specific TripBoundary object.

       This decorator allows access if the user is an admin. Otherwise, it checks if
       the user is the owner of the trip. If the user is not the owner or an admin,
       a 403 Forbidden error is raised.

       Args:
           func: The function to wrap.

       Returns:
           The wrapped function.
       """
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
    """
        Decorator to check if the user has access to a trip by ID.

        This decorator allows access if the user is an admin. Otherwise, it retrieves
        the trip by its ID and checks if the user is the owner. If the user is not the
        owner or an admin, a 403 Forbidden error is raised.

        Args:
            func: The function to wrap.

        Returns:
            The wrapped function.
        """
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
