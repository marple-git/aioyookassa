"""
Tests for payment exceptions.
"""

import pytest

from aioyookassa.exceptions.base import APIError
from aioyookassa.exceptions.payments import NotFound


class TestNotFound:
    """Test NotFound exception."""

    def test_not_found_creation(self):
        """Test NotFound creation."""
        error = NotFound("Not found message")
        assert str(error) == "Not found message"

    def test_not_found_inheritance(self):
        """Test NotFound inheritance."""
        error = NotFound("Not found message")
        assert isinstance(error, APIError)
        assert isinstance(error, Exception)

    def test_not_found_match_pattern(self):
        """Test NotFound match pattern."""
        assert NotFound.match == "not_found"

    def test_not_found_detection(self):
        """Test NotFound detection."""
        with pytest.raises(NotFound):
            APIError.detect("not_found", "Some not found message")

    def test_not_found_case_insensitive_detection(self):
        """Test NotFound case-insensitive detection."""
        with pytest.raises(NotFound):
            APIError.detect("NOT_FOUND", "Some message")

        with pytest.raises(NotFound):
            APIError.detect("Not_Found", "Some message")

    def test_not_found_partial_match(self):
        """Test NotFound partial match."""
        with pytest.raises(NotFound):
            APIError.detect("This is a not_found error", "Some message")

        with pytest.raises(NotFound):
            APIError.detect("not_found_error_code", "Some message")

    def test_not_found_no_match(self):
        """Test NotFound no match."""
        with pytest.raises(APIError):  # Should raise base APIError
            APIError.detect("other_error", "Some message")

    def test_not_found_with_different_contexts(self):
        """Test NotFound with different contexts."""
        # Test with payment not found
        with pytest.raises(NotFound):
            APIError.detect("payment_not_found", "Payment not found")

        # Test with refund not found
        with pytest.raises(NotFound):
            APIError.detect("refund_not_found", "Refund not found")

        # Test with invoice not found
        with pytest.raises(NotFound):
            APIError.detect("invoice_not_found", "Invoice not found")

    def test_not_found_error_messages(self):
        """Test NotFound with different error messages."""
        test_cases = [
            "not_found",
            "NOT_FOUND",
            "Not_Found",
            "payment_not_found",
            "refund_not_found",
            "invoice_not_found",
            "resource_not_found",
            "This is a not_found error message",
            "Error: not_found occurred",
        ]

        for test_case in test_cases:
            with pytest.raises(NotFound):
                APIError.detect(test_case, f"Error message for {test_case}")

    def test_not_found_no_match_cases(self):
        """Test NotFound with cases that should not match."""
        no_match_cases = [
            "found",
            "notfound",
            "not-found",
            "not found",
            "not_found_but_different",
            "other_error",
            "invalid_request",
            "invalid_credentials",
        ]

        for test_case in no_match_cases:
            with pytest.raises(APIError):  # Should raise base APIError
                APIError.detect(test_case, f"Error message for {test_case}")
