from app_setup import create_app
from src.exceptions.exception_handlers import *
from src.exceptions.input_error import InputError
from fastapi.exceptions import RequestValidationError
from src.exceptions.not_found_error import NotFoundError
from fastapi import Request

app = create_app()


@app.exception_handler(NotFoundError)
async def handle_not_found_error(request: Request, exc: NotFoundError):
    return not_found_exception_handler(request, exc)


@app.exception_handler(InputError)
async def handle_input_error(request: Request, exc: InputError):
    return input_error_exception_handler(request, exc)


@app.exception_handler(AuthorizationError)
async def handle_authorization_error(request: Request, exc: AuthorizationError):
    return authorization_exception_handler(request, exc)


@app.exception_handler(AlreadyExistsError)
async def handle_not_found_error(request: Request, exc: AlreadyExistsError):
    return already_exists_exception_handler(request, exc)


@app.exception_handler(ValidationError)
async def handle_validation_error(request: Request, exc: ValidationError):
    return validation_error_exception_handler(request, exc)


@app.exception_handler(InvalidId)
async def handle_invalid_id_error(request: Request, exc: InvalidId):
    return invalid_object_id_exception_handler(request, exc)


@app.exception_handler(ValueError)
async def handle_invalid_id_error(request: Request, exc: ValueError):
    return value_error_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def handle_unprocessable_entity_error(request: Request, exc: RequestValidationError):
    return unprocessable_entity_exception_handler(request, exc)
