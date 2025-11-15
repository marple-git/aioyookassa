"""
Tests for BaseAPI validation improvements.
"""

import pytest

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods.payments import GetPayment
from aioyookassa.types.payment import Payment


class TestBaseAPIValidation:
    """Test BaseAPI validation methods."""

    @pytest.fixture
    def base_api(self):
        """Create BaseAPI instance for testing."""
        client = BaseAPIClient(api_key="test_key", shop_id=123)
        return BaseAPI(client=client)

    @pytest.mark.asyncio
    async def test_get_by_id_with_empty_string(self, base_api):
        """Test _get_by_id raises ValueError for empty string."""
        with pytest.raises(ValueError) as exc_info:
            await base_api._get_by_id(
                resource_id="",
                method_class=GetPayment,
                result_class=Payment,
                id_param_name="payment_id",
            )
        assert "cannot be empty" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_get_by_id_with_whitespace(self, base_api):
        """Test _get_by_id raises ValueError for whitespace-only string."""
        with pytest.raises(ValueError) as exc_info:
            await base_api._get_by_id(
                resource_id="   ",
                method_class=GetPayment,
                result_class=Payment,
                id_param_name="payment_id",
            )
        assert "cannot be empty" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_update_resource_with_empty_string(self, base_api):
        """Test _update_resource raises ValueError for empty string."""
        with pytest.raises(ValueError) as exc_info:
            await base_api._update_resource(
                resource_id="",
                params=None,
                params_class=None,
                method_class=GetPayment,
                result_class=Payment,
                id_param_name="payment_id",
            )
        assert "cannot be empty" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_action_resource_with_empty_string(self, base_api):
        """Test _action_resource raises ValueError for empty string."""
        from aioyookassa.core.methods.payments import CancelPayment

        with pytest.raises(ValueError) as exc_info:
            await base_api._action_resource(
                resource_id="",
                method_class=CancelPayment,
                result_class=Payment,
                id_param_name="payment_id",
            )
        assert "cannot be empty" in str(exc_info.value).lower()
