"""
Tests for PaymentsAPI client.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api.payments import PaymentsAPI
from aioyookassa.types.enum import (
    ConfirmationType,
    Currency,
    PaymentMethodType,
    PaymentStatus,
)
from aioyookassa.types.payment import Payment, PaymentAmount, PaymentsList


@pytest.fixture
def mock_client():
    """Mock BaseAPIClient for testing."""
    client = MagicMock(spec=BaseAPIClient)
    client._send_request = AsyncMock()
    return client


@pytest.fixture
def payments_api(mock_client):
    """PaymentsAPI instance with mocked client."""
    return PaymentsAPI(mock_client)


@pytest.fixture
def sample_payment_data(sample_api_response):
    """Sample payment data for testing."""
    return sample_api_response


@pytest.fixture
def sample_payment_list_data(sample_api_response):
    """Sample payment list data for testing."""
    return {
        "items": [sample_api_response],
        "cursor": "next_cursor_123",
    }


class TestPaymentsAPI:
    """Test PaymentsAPI class."""

    def test_payments_api_initialization(self, mock_client):
        """Test PaymentsAPI initialization."""
        api = PaymentsAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_create_payment_minimal(
        self, payments_api, mock_client, sample_payment_data, sample_payment_amount
    ):
        """Test create_payment with minimal parameters."""
        mock_client._send_request.return_value = sample_payment_data

        result = await payments_api.create_payment(amount=sample_payment_amount)

        assert isinstance(result, Payment)
        assert result.id == "payment_123456789"
        assert result.status == PaymentStatus.SUCCEEDED
        assert result.amount.value == pytest.approx(100.50)

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["amount"]["value"] == pytest.approx(100.50)
        assert call_args[1]["json"]["amount"]["currency"] == "RUB"
        assert "Idempotence-Key" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_create_payment_with_all_parameters(
        self,
        payments_api,
        mock_client,
        sample_payment_data,
        sample_payment_amount,
        sample_payment_method,
        sample_confirmation,
        sample_recipient,
        sample_receipt,
        sample_airline,
        sample_transfer,
        sample_deal,
    ):
        """Test create_payment with all parameters."""
        mock_client._send_request.return_value = sample_payment_data

        result = await payments_api.create_payment(
            amount=sample_payment_amount,
            description="Test payment",
            receipt=sample_receipt,
            recipient=sample_recipient,
            payment_token="payment_token_123",
            payment_method_id="pm_123456789",
            payment_method_data=sample_payment_method,
            confirmation=sample_confirmation,
            save_payment_method=True,
            capture=True,
            client_ip="192.168.1.1",
            metadata={"key": "value"},
            airline=sample_airline,
            transfers=[sample_transfer],
            deal=sample_deal,
            merchant_customer_id="customer_123",
        )

        assert isinstance(result, Payment)

        # Verify the request was made with all parameters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        json_data = call_args[1]["json"]

        assert json_data["amount"]["value"] == pytest.approx(100.50)
        assert json_data["description"] == "Test payment"
        assert json_data["payment_token"] == "payment_token_123"
        assert json_data["save_payment_method"] is True
        assert json_data["capture"] is True
        assert json_data["client_ip"] == "192.168.1.1"
        assert json_data["metadata"] == {"key": "value"}
        assert json_data["merchant_customer_id"] == "customer_123"
        assert "confirmation" in json_data
        assert "receipt" in json_data
        assert "payment_method_data" in json_data
        assert "airline" in json_data
        assert "transfers" in json_data
        assert "deal" in json_data

    @pytest.mark.asyncio
    async def test_get_payments_minimal(
        self, payments_api, mock_client, sample_payment_list_data
    ):
        """Test get_payments with minimal parameters."""
        mock_client._send_request.return_value = sample_payment_list_data

        result = await payments_api.get_payments()

        assert isinstance(result, PaymentsList)
        assert len(result.list) == 1
        assert result.cursor == "next_cursor_123"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["params"] is not None

    @pytest.mark.asyncio
    async def test_get_payments_with_filters(
        self, payments_api, mock_client, sample_payment_list_data
    ):
        """Test get_payments with filters."""
        mock_client._send_request.return_value = sample_payment_list_data

        created_at = datetime(2023, 1, 1, 12, 0, 0)
        captured_at = datetime(2023, 1, 2, 12, 0, 0)

        result = await payments_api.get_payments(
            created_at=created_at,
            captured_at=captured_at,
            payment_method=PaymentMethodType.CARD,
            status=PaymentStatus.SUCCEEDED,
            limit=10,
            cursor="next_cursor_123",
            additional_param="test_value",
        )

        assert isinstance(result, PaymentsList)

        # Verify the request was made with filters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        params = call_args[1]["params"]

        assert params["created_at_gte"] == created_at
        assert params["captured_at_gte"] == captured_at
        assert params["payment_method"] == PaymentMethodType.CARD
        assert params["status"] == PaymentStatus.SUCCEEDED
        assert params["limit"] == 10
        assert params["cursor"] == "next_cursor_123"
        assert params["additional_param"] == "test_value"

    @pytest.mark.asyncio
    async def test_get_payment(self, payments_api, mock_client, sample_payment_data):
        """Test get_payment."""
        mock_client._send_request.return_value = sample_payment_data

        result = await payments_api.get_payment("payment_123456789")

        assert isinstance(result, Payment)
        assert result.id == "payment_123456789"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        # Should be called with GetPayment method instance
        assert hasattr(call_args[0][0], "path")

    @pytest.mark.asyncio
    async def test_capture_payment_minimal(
        self, payments_api, mock_client, sample_payment_data
    ):
        """Test capture_payment with minimal parameters."""
        mock_client._send_request.return_value = sample_payment_data

        result = await payments_api.capture_payment("payment_123456789")

        assert isinstance(result, Payment)

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert "Idempotence-Key" in call_args[1]["headers"]
        assert call_args[1]["json"] == {}

    @pytest.mark.asyncio
    async def test_capture_payment_with_parameters(
        self,
        payments_api,
        mock_client,
        sample_payment_data,
        sample_payment_amount,
        sample_receipt,
        sample_airline,
        sample_transfer,
        sample_deal,
    ):
        """Test capture_payment with parameters."""
        mock_client._send_request.return_value = sample_payment_data

        result = await payments_api.capture_payment(
            "payment_123456789",
            amount=sample_payment_amount,
            receipt=sample_receipt,
            airline=sample_airline,
            transfers=[sample_transfer],
            deal=sample_deal,
        )

        assert isinstance(result, Payment)

        # Verify the request was made with parameters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        json_data = call_args[1]["json"]

        assert json_data["amount"]["value"] == pytest.approx(100.50)
        assert "receipt" in json_data
        assert "airline" in json_data
        assert "transfers" in json_data
        assert "deal" in json_data

    @pytest.mark.asyncio
    async def test_cancel_payment(self, payments_api, mock_client, sample_payment_data):
        """Test cancel_payment."""
        mock_client._send_request.return_value = sample_payment_data

        result = await payments_api.cancel_payment("payment_123456789")

        assert isinstance(result, Payment)

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert "Idempotence-Key" in call_args[1]["headers"]
        # Should not have json data for cancel
        assert "json" not in call_args[1] or call_args[1]["json"] is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method_name,method_args,kwargs",
        [
            (
                "create_payment",
                (),
                {"amount": PaymentAmount(value=100.50, currency=Currency.RUB)},
            ),
            ("get_payments", (), {}),
            ("get_payment", ("payment_123456789",), {}),
            ("capture_payment", ("payment_123456789",), {}),
            ("cancel_payment", ("payment_123456789",), {}),
        ],
    )
    async def test_api_methods_handle_errors(
        self, payments_api, mock_client, method_name, method_args, kwargs
    ):
        """Test API methods handle errors."""
        from aioyookassa.exceptions import APIError

        mock_client._send_request.side_effect = APIError("API Error")

        method = getattr(payments_api, method_name)
        with pytest.raises(APIError):
            await method(*method_args, **kwargs)
