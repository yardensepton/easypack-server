from fastapi import status,HTTPException
from pydantic import ValidationError

from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.input_error import InputError
from src.exceptions.not_found_error import NotFoundError


def not_found_exception_handler(exception: NotFoundError):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception.message))


def input_error_exception_handler(exception: InputError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception.message))

def already_exists_exception_handler(exception: AlreadyExistsError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception.message))


def validation_error_exception_handler(exception: ValidationError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))