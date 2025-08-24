from http import HTTPStatus


class AuthError(Exception):
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthCredentialsError(AuthError):
    def __init__(
        self,
        message: str = "Could not validate credentials or user is inactive",
        status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED,
    ):
        super().__init__(message)
