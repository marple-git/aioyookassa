"""
Webhook-related exceptions.
"""

from aioyookassa.exceptions.base import APIError


class InvalidWebhookIPError(APIError):
    """
    Raised when webhook request comes from an IP address
    that is not in the allowed whitelist.
    """

    def __init__(self, message: str = "IP address not in whitelist"):
        super().__init__(message)
        self.message = message


class InvalidWebhookDataError(APIError):
    """
    Raised when webhook notification data is invalid or cannot be parsed.
    """

    def __init__(self, message: str = "Invalid webhook notification data"):
        super().__init__(message)
        self.message = message
