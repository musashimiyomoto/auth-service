from http import HTTPStatus

from exceptions.base import BaseError


class AuthCredentialsError(BaseError):
    def __init__(
        self,
        message: str = "Could not validate credentials or user is inactive",
        status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED,
    ):
        super().__init__(message=message, status_code=status_code)


class AuthCodeInvalidError(BaseError):
    def __init__(
        self,
        message: str = "Invalid code",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(message=message, status_code=status_code)
