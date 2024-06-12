from bson.errors import InvalidId
from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.authorization_error import AuthorizationError
from src.exceptions.input_error import InputError
from src.exceptions.not_found_error import NotFoundError

def simplify_error_detail(error_detail):
    if "msg" in error_detail[0] and len(error_detail[0]["msg"]) > 0:
        return error_detail[0]["msg"]
    return error_detail  # Return the original error_detail if it doesn't match the expected format

def not_found_exception_handler(request: Request, exception: NotFoundError):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception.message))

def authorization_exception_handler(request: Request, exception: AuthorizationError):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception.message))

def input_error_exception_handler(request: Request, exception: InputError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception.message))

def value_error_exception_handler(request: Request, exception: ValueError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

def already_exists_exception_handler(request: Request, exception: AlreadyExistsError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception.message))

def validation_error_exception_handler(request: Request, exception: ValidationError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))


def invalid_object_id_exception_handler(request: Request, exception: InvalidId):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

def unprocessable_entity_exception_handler(request: Request, exception: RequestValidationError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=simplify_error_detail(exception.errors()))