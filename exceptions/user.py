from http import HTTPStatus

from exceptions.base import BaseError


class UserNotFoundError(BaseError):
    def __init__(
        self,
        message: str = "User not found",
        status_code: HTTPStatus = HTTPStatus.NOT_FOUND,
    ):
        super().__init__(message=message, status_code=status_code)


class UserAlreadyExistsError(BaseError):
    def __init__(
        self,
        message: str = "User already exists",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(message=message, status_code=status_code)


class UserAlreadyActiveError(BaseError):
    def __init__(
        self,
        message: str = "User already active",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(message=message, status_code=status_code)
