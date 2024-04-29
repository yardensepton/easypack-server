from app_setup import create_app
from src.exceptions.exception_handlers import *
from src.exceptions.input_error import InputError
from src.exceptions.not_found_error import NotFoundError
from fastapi import Request
app = create_app()


@app.exception_handler(NotFoundError)
async def handle_not_found_error(exc: NotFoundError):
    return not_found_exception_handler(exc)

@app.exception_handler(InputError)
async def handle_input_error(exc: InputError):
    return input_error_exception_handler(exc)
@app.exception_handler(AlreadyExistsError)
async def handle_not_found_error(exc: AlreadyExistsError):
    return already_exists_exception_handler(exc)

@app.exception_handler(ValidationError)
async def handle_validation_error(exc: ValidationError):
    return validation_error_exception_handler(exc)