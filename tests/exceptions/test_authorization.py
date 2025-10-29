"""
Tests for authorization exceptions.
"""

import pytest

from aioyookassa.exceptions.authorization import InvalidCredentials, InvalidRequestError
from aioyookassa.exceptions.base import APIError


class TestInvalidRequestError:
    """Test InvalidRequestError exception."""

    def test_invalid_request_error_creation(self):
        """Test InvalidRequestError creation."""
        error = InvalidRequestError("Invalid request message")
        assert str(error) == "Invalid request message"

    def test_invalid_request_error_inheritance(self):
        """Test InvalidRequestError inheritance."""
        error = InvalidRequestError("Invalid request message")
        assert isinstance(error, APIError)
        assert isinstance(error, Exception)

    def test_invalid_request_error_match_pattern(self):
        """Test InvalidRequestError match pattern."""
        assert InvalidRequestError.match == "invalid_request"

    def test_invalid_request_error_detection(self):
        """Test InvalidRequestError detection."""
        with pytest.raises(InvalidRequestError):
            APIError.detect("invalid_request", "Some invalid request message")

    def test_invalid_request_error_case_insensitive_detection(self):
        """Test InvalidRequestError case-insensitive detection."""
        with pytest.raises(InvalidRequestError):
            APIError.detect("INVALID_REQUEST", "Some message")

        with pytest.raises(InvalidRequestError):
            APIError.detect("Invalid_Request", "Some message")

    def test_invalid_request_error_partial_match(self):
        """Test InvalidRequestError partial match."""
        with pytest.raises(InvalidRequestError):
            APIError.detect("This is an invalid_request error", "Some message")

        with pytest.raises(InvalidRequestError):
            APIError.detect("invalid_request_error_code", "Some message")

    def test_invalid_request_error_no_match(self):
        """Test InvalidRequestError no match."""
        with pytest.raises(APIError):  # Should raise base APIError
            APIError.detect("other_error", "Some message")


class TestInvalidCredentials:
    """Test InvalidCredentials exception."""

    def test_invalid_credentials_creation(self):
        """Test InvalidCredentials creation."""
        error = InvalidCredentials("Invalid credentials message")
        assert str(error) == "Invalid credentials message"

    def test_invalid_credentials_inheritance(self):
        """Test InvalidCredentials inheritance."""
        error = InvalidCredentials("Invalid credentials message")
        assert isinstance(error, APIError)
        assert isinstance(error, Exception)

    def test_invalid_credentials_match_pattern(self):
        """Test InvalidCredentials match pattern."""
        assert InvalidCredentials.match == "invalid_credentials"

    def test_invalid_credentials_detection(self):
        """Test InvalidCredentials detection."""
        with pytest.raises(InvalidCredentials):
            APIError.detect("invalid_credentials", "Some invalid credentials message")

    def test_invalid_credentials_case_insensitive_detection(self):
        """Test InvalidCredentials case-insensitive detection."""
        with pytest.raises(InvalidCredentials):
            APIError.detect("INVALID_CREDENTIALS", "Some message")

        with pytest.raises(InvalidCredentials):
            APIError.detect("Invalid_Credentials", "Some message")

    def test_invalid_credentials_partial_match(self):
        """Test InvalidCredentials partial match."""
        with pytest.raises(InvalidCredentials):
            APIError.detect("This is an invalid_credentials error", "Some message")

        with pytest.raises(InvalidCredentials):
            APIError.detect("invalid_credentials_error_code", "Some message")

    def test_invalid_credentials_no_match(self):
        """Test InvalidCredentials no match."""
        with pytest.raises(APIError):  # Should raise base APIError
            APIError.detect("other_error", "Some message")


class TestExceptionIntegration:
    """Test exception integration and detection."""

    def test_exception_detection_priority(self):
        """Test that specific exceptions are detected before base exception."""
        # Test InvalidRequestError detection
        with pytest.raises(InvalidRequestError):
            APIError.detect("invalid_request", "Some message")

        # Test InvalidCredentials detection
        with pytest.raises(InvalidCredentials):
            APIError.detect("invalid_credentials", "Some message")

        # Test unknown error falls back to base APIError
        with pytest.raises(APIError):
            APIError.detect("unknown_error", "Some message")

    def test_exception_text_handling(self):
        """Test exception text handling."""

        # Test with custom text
        class TestError(APIError):
            match = "test_error_custom"
            text = "Custom error message"

        with pytest.raises(TestError) as exc_info:
            APIError.detect("test_error_custom", "Original message")
        assert str(exc_info.value) == "Custom error message"

        # Test without custom text (should use original message)
        class TestErrorNoText(APIError):
            match = "test_error_no_text_custom"

        with pytest.raises(TestErrorNoText) as exc_info:
            APIError.detect("test_error_no_text_custom", "Original message")
        assert str(exc_info.value) == "Original message"
