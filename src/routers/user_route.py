from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.controllers import UserController
from src.controllers.trip_controller import TripController
from src.email_notifications.notify import send_reset_password_mail
from src.models.auth_info import AuthInfo
from src.models.user_boundary import UserBoundary
from src.models.user_update import UserUpdate
from src.models.user_entity import UserEntity

from src.utils.authantication.current_identity_utils import get_current_access_identity, \
    get_current_refresh_identity
from src.utils.authantication.jwt_handler import *
from src.utils.decorators.user_decorator import user_permission_check

templates = Jinja2Templates("templates")

router = APIRouter(
    prefix="/users",
    tags=["USERS"]
)

user_controller = UserController()
trip_controller = TripController()


@router.post("/sign-up", response_model=UserEntity)
async def create_user(user: UserBoundary):
    new_user = user_controller.create_user(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=new_user.dict())


@router.post("/login")
async def login_user(user_data: OAuth2PasswordRequestForm = Depends()):
    user_model: AuthInfo = AuthInfo(username=user_data.username, password=user_data.password)
    user_from_db: UserEntity = user_controller.authenticate_user_or_abort(user_model)
    access_token = create_access_token(user_from_db.id)
    refresh_token = create_refresh_token(user_id=user_from_db.id)
    response = JSONResponse(status_code=status.HTTP_200_OK,
                            content={"user_name": user_from_db.name, "user": user_from_db.dict(),
                                     "access_token": access_token,
                                     "refresh_token": refresh_token,
                                     "token_type": "bearer"})
    return response


@router.post("/forgot-password")
async def user_forgot_password(request: Request, user_email: EmailStr):
    user: UserEntity = user_controller.get_user_by_email(user_email)
    if user:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        url = f"{request.base_url}users/reset-password-template?user_email={user_email}&time={current_time}"

        await send_reset_password_mail(recipient_email=user_email, user=user, url=url,
                                       expire_in_minutes=RESET_PASSWORD_TIME_EXPIRE)
        return {
            "result": f"An email has been sent to {user_email} with a link for password reset."
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/reset-password-template")
async def user_reset_password_template(request: Request):
    try:
        user_email = request.query_params.get('user_email')
        time = request.query_params.get('time')
        current_time = datetime.now()
        given_datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        time_difference = current_time - given_datetime
        is_success = time_difference <= timedelta(minutes=RESET_PASSWORD_TIME_EXPIRE)
        response = templates.TemplateResponse(
            "reset_password.html",
            {
                "request": request,
                "user_email": user_email,
                "time": time,
                "success": is_success
            }
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.post("/reset-password")
async def user_reset_password(request: Request, new_password: str = Form(...), user_email: str = Form(...)):
    if not user_email:
        raise HTTPException(status_code=401, detail="No user details")
    try:
        user: UserEntity = user_controller.get_user_by_email(user_email)
        result = user_controller.user_reset_password(new_password, user)
        response = templates.TemplateResponse(
            "reset_password_result.html",
            {
                "request": request,
                "success": result
            }
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.post("/refresh")
async def refresh_new_token(refresh_token: str):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    user: UserEntity = await get_current_refresh_identity(refresh_token)
    access_token = create_access_token(user_id=user.id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token,
                                                                 "token_type": "bearer"})


@router.get("", response_model=UserEntity)
@user_permission_check
async def get_user_by_id(identity: UserEntity = Depends(get_current_access_identity)):
    user = await user_controller.get_user_by_id(identity.id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.dict())


@router.delete("/{user_id}")
@user_permission_check
async def delete_user_by_id(user_id: str, identity: UserEntity = Depends(get_current_access_identity)):
    await user_controller.get_user_by_id(user_id)
    await trip_controller.delete_trips_by_user_id(user_id)
    user_controller.delete_user_by_id(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"user {user_id} deleted")


@router.put("", response_model=UserEntity)
# @user_permission_check
async def update_user_by_id(new_info: UserUpdate,
                            identity: UserEntity = Depends(get_current_access_identity)):
    updated_user: UserEntity = user_controller.update_user_by_id(new_info, identity)
    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_user.dict())
