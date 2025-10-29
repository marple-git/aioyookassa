from .base import APIError


class InvalidRequestError(APIError):
    """Invalid request error"""

    match = "invalid_request"


class InvalidCredentials(APIError):
    """Invalid credentials error"""

    match = "invalid_credentials"
