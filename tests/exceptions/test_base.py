"""
Tests for base exception classes.
"""

import pytest

from aioyookassa.exceptions.base import APIError, _MatchErrorMixin
from aioyookassa.exceptions.payments import NotFound


class TestAPIError:
    """Test APIError exception."""

    def test_api_error_creation(self):
        """Test APIError creation."""
        error = APIError("Test error message")
        assert str(error) == "Test error message"

    def test_api_error_inheritance(self):
        """Test APIError inheritance."""
        error = APIError("Test error message")
        assert isinstance(error, Exception)
        assert isinstance(error, _MatchErrorMixin)


class TestMatchErrorMixin:
    """Test _MatchErrorMixin functionality."""

    def test_match_error_mixin_check_method(self):
        """Test _MatchErrorMixin check method."""

        class TestError(APIError):
            match = "test_error"

        # Test case-insensitive matching (method expects lowercase)
        assert TestError.check("test_error") is True
        assert TestError.check("test_error") is True  # Already lowercase
        assert TestError.check("this is a test_error message") is True
        assert TestError.check("other_error") is False

    def test_match_error_mixin_get_text_method(self):
        """Test _MatchErrorMixin get_text method."""

        class TestError(APIError):
            match = "test_error"
            text = "Custom error text"

        # Test with custom text
        assert TestError.get_text("original message") == "Custom error text"

        # Test without custom text
        class TestErrorNoText(APIError):
            match = "test_error"

        assert TestErrorNoText.get_text("original message") == "original message"

    def test_match_error_mixin_detect_method(self):
        """Test _MatchErrorMixin detect method."""

        class TestError1(APIError):
            match = "error1"
            text = "Error 1 occurred"

        class TestError2(APIError):
            match = "error2"
            text = "Error 2 occurred"

        # Test detection of specific error
        with pytest.raises(TestError1) as exc_info:
            APIError.detect("error1", "Some error1 message")
        assert str(exc_info.value) == "Error 1 occurred"

        with pytest.raises(TestError2) as exc_info:
            APIError.detect("error2", "Some error2 message")
        assert str(exc_info.value) == "Error 2 occurred"

        # Test detection of unknown error (should raise base class)
        with pytest.raises(APIError) as exc_info:
            APIError.detect("unknown_error", "Some unknown error message")
        assert str(exc_info.value) == "unknown_error"

    def test_match_error_mixin_subclass_registration(self):
        """Test that subclasses are automatically registered."""
        # Clear existing subclasses for clean test
        original_subclasses = APIError._MatchErrorMixin__subclasses.copy()
        APIError._MatchErrorMixin__subclasses.clear()

        try:

            class TestError1(APIError):
                match = "error1"

            class TestError2(APIError):
                match = "error2"

            # Check that subclasses are registered
            assert len(APIError._MatchErrorMixin__subclasses) == 2
            assert TestError1 in APIError._MatchErrorMixin__subclasses
            assert TestError2 in APIError._MatchErrorMixin__subclasses

        finally:
            # Restore original subclasses
            APIError._MatchErrorMixin__subclasses.clear()
            APIError._MatchErrorMixin__subclasses.extend(original_subclasses)

    def test_match_error_mixin_case_insensitive_detection(self):
        """Test that detection is case-insensitive."""
        # Test with existing exceptions to avoid conflicts
        with pytest.raises(NotFound):
            APIError.detect("NOT_FOUND", "Some message")

        with pytest.raises(NotFound):
            APIError.detect("Not_Found", "Some message")

        with pytest.raises(NotFound):
            APIError.detect("not_found", "Some message")

    def test_match_error_mixin_empty_match_string(self):
        """Test behavior with empty match string."""

        class TestError(APIError):
            match = ""

        # Empty match should not match anything
        assert TestError.check("any message") is False
        assert TestError.check("") is False  # Empty string should not match anything

    def test_match_error_mixin_none_text(self):
        """Test behavior when text is None."""

        class TestError(APIError):
            match = "test_error"
            text = None

        # Should return the original message when text is None
        assert TestError.get_text("original message") == "original message"

    def test_match_error_mixin_with_error_details(self):
        """Test _MatchErrorMixin with detailed error information from API."""
        from aioyookassa.exceptions.authorization import InvalidRequestError

        # Test with error details including parameter
        error_details = {
            "code": "invalid_request",
            "description": "Invalid parameter value",
            "parameter": "confirmation.return_url",
            "type": "validation_error",
        }
        with pytest.raises(InvalidRequestError) as exc_info:
            APIError.detect(
                "invalid_request",
                "Invalid parameter value",
                error_details=error_details,
            )
        error_message = str(exc_info.value)
        assert "Invalid parameter value" in error_message
        assert "Parameter: confirmation.return_url" in error_message
        assert "Type: validation_error" in error_message

        # Test with error details including retry_after
        error_details_retry = {
            "code": "rate_limit_exceeded",
            "description": "Too many requests",
            "retry_after": 60,
        }
        with pytest.raises(APIError) as exc_info:
            APIError.detect(
                "rate_limit_exceeded",
                "Too many requests",
                error_details=error_details_retry,
            )
        error_message = str(exc_info.value)
        assert "Too many requests" in error_message
        assert "Retry after: 60" in error_message
