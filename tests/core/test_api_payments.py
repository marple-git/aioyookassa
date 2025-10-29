"""
Tests for PaymentsAPI client.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from aioyookassa.core.api.payments import PaymentsAPI
from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.types.payment import (
    PaymentAmount, Payment, PaymentMethod, CardInfo, Confirmation,
    Recipient, Receipt, PaymentItem, Customer, Airline, Transfer, Deal,
    PaymentsList
)
from aioyookassa.types.enum import (
    PaymentMethodType, ConfirmationType, Currency, PaymentStatus,
    PaymentSubject, PaymentMode
)


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
def sample_payment_data():
    """Sample payment data for testing."""
    return {
        "id": "payment_123456789",
        "status": "succeeded",
        "amount": {"value": 100.50, "currency": "RUB"},
        "description": "Test payment",
        "recipient": {"account_id": "123456", "gateway_id": "gateway_123"},
        "payment_method": {
            "type": "bank_card",
            "id": "pm_123456789",
            "saved": True,
            "title": "Test Card",
            "card": {
                "last4": "1234",
                "expiry_year": "2025",
                "expiry_month": "12",
                "card_type": "Visa"
            }
        },
        "created_at": "2023-01-01T00:00:00.000Z",
        "test": True,
        "paid": True,
        "refundable": True
    }


@pytest.fixture
def sample_payment_list_data():
    """Sample payment list data for testing."""
    return {
        "items": [{
            "id": "payment_123456789",
            "status": "succeeded",
            "amount": {"value": 100.50, "currency": "RUB"},
            "description": "Test payment",
            "recipient": {"account_id": "123456", "gateway_id": "gateway_123"},
            "payment_method": {
                "type": "bank_card",
                "id": "pm_123456789",
                "saved": True,
                "title": "Test Card",
                "card": {
                    "last4": "1234",
                    "expiry_year": "2025",
                    "expiry_month": "12",
                    "card_type": "Visa"
                }
            },
            "created_at": "2023-01-01T00:00:00.000Z",
            "test": True,
            "paid": True,
            "refundable": True
        }],
        "cursor": "next_cursor_123"
    }






class TestPaymentsAPI:
    """Test PaymentsAPI class."""

    def test_payments_api_initialization(self, mock_client):
        """Test PaymentsAPI initialization."""
        api = PaymentsAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_create_payment_minimal(self, payments_api, mock_client, sample_payment_data):
        """Test create_payment with minimal parameters."""
        mock_client._send_request.return_value = sample_payment_data
        
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        result = await payments_api.create_payment(amount=amount)
        
        assert isinstance(result, Payment)
        assert result.id == "payment_123456789"
        assert result.status == PaymentStatus.SUCCEEDED
        assert result.amount.value == 100.50
        
        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["amount"]["value"] == 100.50
        assert call_args[1]["json"]["amount"]["currency"] == "RUB"
        assert "Idempotence-Key" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_create_payment_with_all_parameters(self, payments_api, mock_client, sample_payment_data):
        """Test create_payment with all parameters."""
        mock_client._send_request.return_value = sample_payment_data
        
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        card = CardInfo(
            last4="1234",
            expiry_year="2025",
            expiry_month="12",
            card_type="Visa"
        )
        payment_method = PaymentMethod(
            type=PaymentMethodType.CARD,
            id="pm_123456789",
            saved=True,
            card=card
        )
        confirmation = Confirmation(
            type=ConfirmationType.REDIRECT,
            return_url="https://example.com/return"
        )
        recipient = Recipient(account_id="123456", gateway_id="gateway_123")
        customer = Customer(full_name="John Doe", email="john@example.com")
        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT
        )
        receipt = Receipt(customer=customer, items=[item])
        airline = Airline(ticket_number="TK123456", booking_reference="ABC123")
        transfer = Transfer(
            account_id="123456",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PaymentStatus.SUCCEEDED
        )
        deal = Deal(
            id="deal_123456789",
            settlements=[PaymentAmount(value=100.50, currency=Currency.RUB)]
        )
        
        result = await payments_api.create_payment(
            amount=amount,
            description="Test payment",
            receipt=receipt,
            recipient=recipient,
            payment_token="payment_token_123",
            payment_method_id="pm_123456789",
            payment_method_data=payment_method,
            confirmation=confirmation,
            save_payment_method=True,
            capture=True,
            client_ip="192.168.1.1",
            metadata={"key": "value"},
            airline=airline,
            transfers=[transfer],
            deal=deal,
            merchant_customer_id="customer_123"
        )
        
        assert isinstance(result, Payment)
        
        # Verify the request was made with all parameters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        json_data = call_args[1]["json"]
        
        assert json_data["amount"]["value"] == 100.50
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
    async def test_get_payments_minimal(self, payments_api, mock_client, sample_payment_list_data):
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
    async def test_get_payments_with_filters(self, payments_api, mock_client, sample_payment_list_data):
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
            additional_param="test_value"
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
        assert hasattr(call_args[0][0], 'path')

    @pytest.mark.asyncio
    async def test_capture_payment_minimal(self, payments_api, mock_client, sample_payment_data):
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
    async def test_capture_payment_with_parameters(self, payments_api, mock_client, sample_payment_data):
        """Test capture_payment with parameters."""
        mock_client._send_request.return_value = sample_payment_data
        
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        customer = Customer(full_name="John Doe", email="john@example.com")
        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT
        )
        receipt = Receipt(customer=customer, items=[item])
        airline = Airline(ticket_number="TK123456", booking_reference="ABC123")
        transfer = Transfer(
            account_id="123456",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PaymentStatus.SUCCEEDED
        )
        deal = Deal(
            id="deal_123456789",
            settlements=[PaymentAmount(value=100.50, currency=Currency.RUB)]
        )
        
        result = await payments_api.capture_payment(
            "payment_123456789",
            amount=amount,
            receipt=receipt,
            airline=airline,
            transfers=[transfer],
            deal=deal
        )
        
        assert isinstance(result, Payment)
        
        # Verify the request was made with parameters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        json_data = call_args[1]["json"]
        
        assert json_data["amount"]["value"] == 100.50
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
    async def test_create_payment_handles_api_errors(self, payments_api, mock_client):
        """Test create_payment handles API errors."""
        from aioyookassa.exceptions import APIError
        
        mock_client._send_request.side_effect = APIError("API Error")
        
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        
        with pytest.raises(APIError):
            await payments_api.create_payment(amount=amount)

    @pytest.mark.asyncio
    async def test_get_payments_handles_api_errors(self, payments_api, mock_client):
        """Test get_payments handles API errors."""
        from aioyookassa.exceptions import APIError
        
        mock_client._send_request.side_effect = APIError("API Error")
        
        with pytest.raises(APIError):
            await payments_api.get_payments()

    @pytest.mark.asyncio
    async def test_get_payment_handles_api_errors(self, payments_api, mock_client):
        """Test get_payment handles API errors."""
        from aioyookassa.exceptions import APIError
        
        mock_client._send_request.side_effect = APIError("API Error")
        
        with pytest.raises(APIError):
            await payments_api.get_payment("payment_123456789")

    @pytest.mark.asyncio
    async def test_capture_payment_handles_api_errors(self, payments_api, mock_client):
        """Test capture_payment handles API errors."""
        from aioyookassa.exceptions import APIError
        
        mock_client._send_request.side_effect = APIError("API Error")
        
        with pytest.raises(APIError):
            await payments_api.capture_payment("payment_123456789")

    @pytest.mark.asyncio
    async def test_cancel_payment_handles_api_errors(self, payments_api, mock_client):
        """Test cancel_payment handles API errors."""
        from aioyookassa.exceptions import APIError
        
        mock_client._send_request.side_effect = APIError("API Error")
        
        with pytest.raises(APIError):
            await payments_api.cancel_payment("payment_123456789")
