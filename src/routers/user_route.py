from fastapi import APIRouter

from src.controllers import UserController
from src.controllers.trip_controller import TripController
from src.entity.update_user import UserUpdate
from src.entity.user import User

router = APIRouter(
    prefix="/users",
    tags=["USERS"]
)

user_controller = UserController()
trip_controller = TripController()


@router.post("", response_model=User)
def create_user(user: User):
    return user_controller.create_user(user)


# @router.get("/by", response_model=User)
# def get_user_by_email(email: str = Query(..., alias="email")):
#     return user_controller.get_user_by_email(email)


@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: str):
    return user_controller.get_user_by_id(user_id)


# @router.delete("/{user_id}", response_model=None)
# def delete_user_by_id(user_id: str):
#     trip_controller.delete_trip_by_id()
#     user_controller.delete_user_by_id(user_id)

@router.delete("/{user_id}", response_model=None)
def delete_user_by_id(user_id: str):
    trip_controller.delete_trips_by_user_id(user_id)
    user_controller.delete_user_by_id(user_id)


@router.put("/{user_id}", response_model=User)
def update_user_by_id(new_info: UserUpdate, user_id: str):
    return user_controller.update_user_by_id(new_info, user_id)
