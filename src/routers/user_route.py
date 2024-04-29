from fastapi import APIRouter


from src.controllers import UserController
from src.controllers.trip_controller import TripController
from src.entity.user_schema import UserSchema
from src.entity.user import User

router = APIRouter(
    prefix="/users",
    tags=["USERS"]
)

user_controller = UserController()
trip_controller = TripController()


@router.post("", response_model=User)
async def create_user(user: User):
    return user_controller.create_user(user)


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    return user_controller.get_user_by_id(user_id)


@router.delete("/{user_id}", response_model=None)
async def delete_user_by_id(user_id: str):
    user_controller.get_user_by_id(user_id)
    trip_controller.delete_trips_by_user_id(user_id)
    user_controller.delete_user_by_id(user_id)


@router.put("/{user_id}", response_model=User)
async def update_user_by_id(new_info: UserSchema, user_id: str):
    return user_controller.update_user_by_id(new_info, user_id)
