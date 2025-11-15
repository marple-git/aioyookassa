"""
Tests for self-employed methods.
"""

import pytest

from aioyookassa.core.methods.self_employed import (
    CreateSelfEmployed,
    GetSelfEmployed,
    SelfEmployedAPIMethod,
)
from aioyookassa.types.params import SelfEmployedConfirmationData


class TestSelfEmployedAPIMethod:
    """Test SelfEmployedAPIMethod base class."""

    def test_self_employed_api_method_initialization(self):
        """Test SelfEmployedAPIMethod initialization."""
        method = SelfEmployedAPIMethod()
        assert method.http_method == "GET"
        assert method.path == "/self_employed"

    def test_self_employed_api_method_with_custom_path(self):
        """Test SelfEmployedAPIMethod with custom path."""
        method = SelfEmployedAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_self_employed_api_method_build(self):
        """Test SelfEmployedAPIMethod build method."""
        method = SelfEmployedAPIMethod.build("se_123")
        assert method.path == "/self_employed"  # Should use class path

    def test_self_employed_api_method_build_with_format(self):
        """Test SelfEmployedAPIMethod build with path formatting."""

        class TestMethod(SelfEmployedAPIMethod):
            path = "/self_employed/{self_employed_id}"

        method = TestMethod.build("se_123")
        assert method.path == "/self_employed/se_123"


class TestCreateSelfEmployed:
    """Test CreateSelfEmployed method."""

    def test_create_self_employed_initialization(self):
        """Test CreateSelfEmployed initialization."""
        method = CreateSelfEmployed()
        assert method.http_method == "POST"
        assert method.path == "/self_employed"

    def test_create_self_employed_build_params_minimal_with_itn(self):
        """Test CreateSelfEmployed build_params with ITN only."""
        params = CreateSelfEmployed.build_params(itn="123456789012")

        assert params == {"itn": "123456789012"}

    def test_create_self_employed_build_params_minimal_with_phone(self):
        """Test CreateSelfEmployed build_params with phone only."""
        params = CreateSelfEmployed.build_params(phone="79000000000")

        assert params == {"phone": "79000000000"}

    def test_create_self_employed_build_params_with_confirmation(self):
        """Test CreateSelfEmployed build_params with confirmation."""
        confirmation = SelfEmployedConfirmationData(
            confirmation_url="https://example.com/confirm"
        )

        params = CreateSelfEmployed.build_params(
            itn="123456789012", confirmation=confirmation
        )

        assert params["itn"] == "123456789012"
        assert params["confirmation"]["type"] == "redirect"
        assert (
            params["confirmation"]["confirmation_url"] == "https://example.com/confirm"
        )

    def test_create_self_employed_build_params_with_all_fields(self):
        """Test CreateSelfEmployed build_params with all fields."""
        confirmation = SelfEmployedConfirmationData(
            confirmation_url="https://example.com/confirm"
        )

        params = CreateSelfEmployed.build_params(
            itn="123456789012",
            phone="79000000000",
            confirmation=confirmation,
        )

        assert params["itn"] == "123456789012"
        assert params["phone"] == "79000000000"
        assert params["confirmation"]["type"] == "redirect"
        assert (
            params["confirmation"]["confirmation_url"] == "https://example.com/confirm"
        )

    def test_create_self_employed_build_params_filters_none_values(self):
        """Test CreateSelfEmployed build_params filters out None values."""
        params = CreateSelfEmployed.build_params(
            itn=None, phone=None, confirmation=None
        )

        # All values are None, so should be filtered out
        expected = {}
        assert params == expected


class TestGetSelfEmployed:
    """Test GetSelfEmployed method."""

    def test_get_self_employed_initialization(self):
        """Test GetSelfEmployed initialization."""
        method = GetSelfEmployed()
        assert method.http_method == "GET"
        assert method.path == "/self_employed/{self_employed_id}"

    def test_get_self_employed_build(self):
        """Test GetSelfEmployed build method."""
        method = GetSelfEmployed.build("se_123")
        assert method.path == "/self_employed/se_123"
