from bson.errors import InvalidId
from fastapi import Request

from fastapi import status,HTTPException
from pydantic import ValidationError

from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.input_error import InputError
from src.exceptions.not_found_error import NotFoundError


def not_found_exception_handler(request: Request, exception: NotFoundError):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception.message))


def input_error_exception_handler(request :Request,exception: InputError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception.message))

def value_error_exception_handler(request :Request,exception: ValueError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

def already_exists_exception_handler(request :Request,exception: AlreadyExistsError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception.message))


def validation_error_exception_handler(request :Request,exception: ValidationError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))


def invalid_object_id_exception_handler(request :Request,exception: InvalidId):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))