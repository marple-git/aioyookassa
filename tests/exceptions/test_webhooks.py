"""
Tests for webhook-related exceptions.
"""

import pytest

from aioyookassa.exceptions.base import APIError
from aioyookassa.exceptions.webhooks import InvalidWebhookDataError, InvalidWebhookIPError


class TestInvalidWebhookIPError:
    """Test InvalidWebhookIPError exception."""

    def test_invalid_webhook_ip_error_creation_default(self):
        """Test InvalidWebhookIPError creation with default message."""
        error = InvalidWebhookIPError()
        assert str(error) == "IP address not in whitelist"
        assert error.message == "IP address not in whitelist"

    def test_invalid_webhook_ip_error_creation_custom(self):
        """Test InvalidWebhookIPError creation with custom message."""
        custom_message = "Custom IP error message"
        error = InvalidWebhookIPError(custom_message)
        assert str(error) == custom_message
        assert error.message == custom_message

    def test_invalid_webhook_ip_error_inheritance(self):
        """Test InvalidWebhookIPError inheritance."""
        error = InvalidWebhookIPError()
        assert isinstance(error, Exception)
        assert isinstance(error, APIError)


class TestInvalidWebhookDataError:
    """Test InvalidWebhookDataError exception."""

    def test_invalid_webhook_data_error_creation_default(self):
        """Test InvalidWebhookDataError creation with default message."""
        error = InvalidWebhookDataError()
        assert str(error) == "Invalid webhook notification data"
        assert error.message == "Invalid webhook notification data"

    def test_invalid_webhook_data_error_creation_custom(self):
        """Test InvalidWebhookDataError creation with custom message."""
        custom_message = "Custom data error message"
        error = InvalidWebhookDataError(custom_message)
        assert str(error) == custom_message
        assert error.message == custom_message

    def test_invalid_webhook_data_error_inheritance(self):
        """Test InvalidWebhookDataError inheritance."""
        error = InvalidWebhookDataError()
        assert isinstance(error, Exception)
        assert isinstance(error, APIError)

