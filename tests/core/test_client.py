"""
Tests for YooKassa client.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.client import YooKassa


class TestYooKassa:
    """Test YooKassa client."""

    def test_yookassa_initialization(self):
        """Test YooKassa initialization."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        assert client.api_key == "test_api_key"
        assert client.shop_id == "123456"
        assert hasattr(client, "payments")
        assert hasattr(client, "payment_methods")
        assert hasattr(client, "invoices")
        assert hasattr(client, "refunds")
        assert hasattr(client, "receipts")

    def test_yookassa_initialization_with_string_shop_id(self):
        """Test YooKassa initialization with string shop_id."""
        client = YooKassa(api_key="test_api_key", shop_id="123456")

        assert client.api_key == "test_api_key"
        assert client.shop_id == "123456"  # Should be converted to string

    def test_yookassa_initialization_with_int_shop_id(self):
        """Test YooKassa initialization with int shop_id."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        assert client.api_key == "test_api_key"
        assert client.shop_id == "123456"  # Should be converted to string

    def test_yookassa_inheritance(self):
        """Test YooKassa inheritance from BaseAPIClient."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        assert isinstance(client, BaseAPIClient)

    def test_yookassa_api_modules_initialization(self):
        """Test that all API modules are properly initialized."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        # Check that all API modules are initialized
        assert client.payments is not None
        assert client.payment_methods is not None
        assert client.invoices is not None
        assert client.refunds is not None
        assert client.receipts is not None

        # Check that all API modules have the client reference
        assert client.payments._client == client
        assert client.payment_methods._client == client
        assert client.invoices._client == client
        assert client.refunds._client == client
        assert client.receipts._client == client

    def test_yookassa_base_url(self):
        """Test YooKassa base URL."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        assert client.BASE_URL == "https://api.yookassa.ru/v3"

    def test_yookassa_credentials_storage(self):
        """Test that credentials are stored correctly."""
        api_key = "test_api_key_12345"
        shop_id = 987654

        client = YooKassa(api_key=api_key, shop_id=shop_id)

        assert client.api_key == api_key
        assert client.shop_id == str(shop_id)  # Should be converted to string

    def test_yookassa_with_different_shop_id_types(self):
        """Test YooKassa with different shop_id types."""
        # Test with string
        client1 = YooKassa(api_key="test_api_key", shop_id="123456")
        assert client1.shop_id == "123456"

        # Test with int
        client2 = YooKassa(api_key="test_api_key", shop_id=123456)
        assert client2.shop_id == "123456"

        # Test with float (should be converted to string)
        client3 = YooKassa(api_key="test_api_key", shop_id=123456.0)
        assert client3.shop_id == "123456.0"

    def test_yookassa_api_modules_types(self):
        """Test that API modules are of correct types."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        # Import the API classes to check types
        from aioyookassa.core.api.invoices import InvoicesAPI
        from aioyookassa.core.api.payment_methods import PaymentMethodsAPI
        from aioyookassa.core.api.payments import PaymentsAPI
        from aioyookassa.core.api.receipts import ReceiptsAPI
        from aioyookassa.core.api.refunds import RefundsAPI

        assert isinstance(client.payments, PaymentsAPI)
        assert isinstance(client.payment_methods, PaymentMethodsAPI)
        assert isinstance(client.invoices, InvoicesAPI)
        assert isinstance(client.refunds, RefundsAPI)
        assert isinstance(client.receipts, ReceiptsAPI)

    def test_yookassa_session_management(self):
        """Test YooKassa session management."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        # Initially session should be None
        assert client._session is None

        # Test that session can be created (mocked)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(client, "_get_session", MagicMock())
            session = client._get_session()
            assert session is not None

    @pytest.mark.asyncio
    async def test_yookassa_close_method(self):
        """Test YooKassa close method."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        # Mock session
        mock_session = AsyncMock()
        mock_session.closed = False
        client._session = mock_session

        # Test close method
        await client.close()

        # Session should be closed
        mock_session.close.assert_called_once()
        assert client._session is None

    def test_yookassa_context_manager(self):
        """Test YooKassa as context manager."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        # Test async context manager
        import asyncio

        async def test_context_manager():
            async with client as ctx:
                assert ctx is client
                assert ctx.api_key == "test_api_key"
                assert ctx.shop_id == "123456"

        asyncio.run(test_context_manager())

    def test_yookassa_api_modules_independence(self):
        """Test that API modules are independent instances."""
        client = YooKassa(api_key="test_api_key", shop_id=123456)

        # Each API module should be a separate instance
        assert client.payments is not client.payment_methods
        assert client.payments is not client.invoices
        assert client.payments is not client.refunds
        assert client.payments is not client.receipts

        # But all should reference the same client
        assert client.payments._client is client
        assert client.payment_methods._client is client
        assert client.invoices._client is client
        assert client.refunds._client is client
        assert client.receipts._client is client
