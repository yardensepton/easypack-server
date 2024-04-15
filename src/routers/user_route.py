from fastapi import APIRouter, HTTPException
from starlette import status

from src.controllers import UserController
from src.controllers.trip_controller import TripController
from src.entity.update_user import UserUpdate
from src.entity.user import User
from src.exceptions.input_error import InputError
from src.exceptions.user_already_exists_error import UserAlreadyExistsError
from src.exceptions.user_not_found_error import UserNotFoundError

router = APIRouter(
    prefix="/users",
    tags=["USERS"]
)

user_controller = UserController()
trip_controller = TripController()


@router.post("", response_model=User)
def create_user(user: User):
    try:
        return user_controller.create_user(user)
    except InputError as ie:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ie))
    except UserAlreadyExistsError as uae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(uae))


@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: str):
    try:
        return user_controller.get_user_by_id(user_id)
    except UserNotFoundError as unf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(unf))

@router.delete("/{user_id}", response_model=None)
def delete_user_by_id(user_id: str):
    try:
        user_controller.get_user_by_id(user_id)
        trip_controller.delete_trips_by_user_id(user_id)
        user_controller.delete_user_by_id(user_id)
    except UserNotFoundError as unf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(unf))



@router.put("/{user_id}", response_model=User)
def update_user_by_id(new_info: UserUpdate, user_id: str):
    try:
        return user_controller.update_user_by_id(new_info, user_id)
    except UserNotFoundError as unf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(unf))

