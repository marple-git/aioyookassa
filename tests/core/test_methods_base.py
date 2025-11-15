"""
Tests for base API methods.
"""

import pytest

from aioyookassa.core.methods.base import APIMethod, BaseAPIMethod


class TestBaseAPIMethod:
    """Test BaseAPIMethod class."""

    def test_base_api_method_initialization(self):
        """Test BaseAPIMethod initialization."""
        method = BaseAPIMethod()
        assert method.http_method == "GET"
        # BaseAPIMethod doesn't have path attribute by default
        # It's set in subclasses or via __init__

    def test_base_api_method_with_custom_path(self):
        """Test BaseAPIMethod with custom path."""
        method = BaseAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_base_api_method_build_without_kwargs(self):
        """Test BaseAPIMethod build without kwargs."""
        method = BaseAPIMethod.build()
        assert isinstance(method, BaseAPIMethod)

    def test_base_api_method_build_with_format(self):
        """Test BaseAPIMethod build with path formatting."""

        class TestMethod(BaseAPIMethod):
            path = "/test/{test_id}"

        method = TestMethod.build(test_id="test_123")
        assert method.path == "/test/test_123"

    def test_base_api_method_build_missing_parameter(self):
        """Test BaseAPIMethod build with missing parameter raises ValueError."""

        class TestMethod(BaseAPIMethod):
            path = "/test/{test_id}"

        with pytest.raises(ValueError) as exc_info:
            TestMethod.build(wrong_param="test_123")

        assert "Missing required parameter" in str(exc_info.value)
        assert "test_id" in str(exc_info.value)

    def test_base_api_method_build_invalid_format(self):
        """Test BaseAPIMethod build with invalid format raises ValueError."""

        class TestMethod(BaseAPIMethod):
            path = "/test/{test_id}/{invalid}"

        with pytest.raises(ValueError) as exc_info:
            TestMethod.build(test_id="test_123")

        # Missing parameter is caught as KeyError and converted to ValueError
        assert "Missing required parameter" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    def test_safe_model_dump_with_none(self):
        """Test _safe_model_dump with None."""
        result = APIMethod._safe_model_dump(None)
        assert result is None

    def test_safe_model_dump_with_dict(self):
        """Test _safe_model_dump with dict."""
        data = {"key": "value"}
        result = APIMethod._safe_model_dump(data)
        assert result == data
        assert result is data  # Should return same object
