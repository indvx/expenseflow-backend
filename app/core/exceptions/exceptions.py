from fastapi import status


class AppException(Exception):
    status_code = 400
    message = "Application error"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message


class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "User not found"


class InvalidCredentialsException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid email or password"


class RateLimitException(AppException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    message = "Too many requests. Please try again later."


class InvalidTokenException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid or expired token"


class ForbiddenException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "You do not have permission to perform this action"


class AlreadyExistsException(AppException):
    status_code = status.HTTP_409_CONFLICT
    message = "User already exists"

    def __init__(self, field: str, message: str | None = None):
        if message:
            self.message = message
        else:
            self.message = f"{field} already exists"


class InvalidFileFormatException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Invalid file format. Please upload a valid CSV file."
