"""
Tests for SBP banks methods.
"""

import pytest

from aioyookassa.core.methods.sbp_banks import GetSbpBanks, SbpBanksAPIMethod


class TestSbpBanksAPIMethod:
    """Test SbpBanksAPIMethod base class."""

    def test_sbp_banks_api_method_initialization(self):
        """Test SbpBanksAPIMethod initialization."""
        method = SbpBanksAPIMethod()
        assert method.http_method == "GET"
        assert method.path == "/sbp_banks"

    def test_sbp_banks_api_method_with_custom_path(self):
        """Test SbpBanksAPIMethod with custom path."""
        method = SbpBanksAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_sbp_banks_api_method_build(self):
        """Test SbpBanksAPIMethod build method (no ID needed)."""
        method = SbpBanksAPIMethod.build()
        assert method.path == "/sbp_banks"


class TestGetSbpBanks:
    """Test GetSbpBanks method."""

    def test_get_sbp_banks_initialization(self):
        """Test GetSbpBanks initialization."""
        method = GetSbpBanks()
        assert method.http_method == "GET"
        assert method.path == "/sbp_banks"

    def test_get_sbp_banks_build_params(self):
        """Test GetSbpBanks build_params (no parameters)."""
        params = GetSbpBanks.build_params()

        # Should return empty dict as there are no parameters
        expected = {}
        assert params == expected

    def test_get_sbp_banks_build_params_with_kwargs(self):
        """Test GetSbpBanks build_params ignores kwargs (no parameters)."""
        params = GetSbpBanks.build_params(any_param="value", another_param=123)

        # Should return empty dict regardless of kwargs
        expected = {}
        assert params == expected
