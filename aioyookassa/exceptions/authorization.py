from .base import APIError


class InvalidRequestError(APIError):
    """Invalid request error"""
    match = "invalid_request"
