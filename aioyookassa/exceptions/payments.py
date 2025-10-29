from .base import APIError


class NotFound(APIError):
    """Not found error"""

    match = "not_found"
