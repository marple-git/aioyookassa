"""
Tests for PayoutsAPI client.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api.payouts import PayoutsAPI
from aioyookassa.types.enum import Currency, PayoutStatus
from aioyookassa.types.params import (
    BankCardPayoutCardData,
    BankCardPayoutDestinationData,
    CreatePayoutParams,
    PayoutReceiptData,
)
from aioyookassa.types.payment import Deal, PaymentAmount
from aioyookassa.types.payout import Payout, SelfEmployed


@pytest.fixture
def mock_client():
    """Mock BaseAPIClient for testing."""
    client = MagicMock(spec=BaseAPIClient)
    client._send_request = AsyncMock()
    return client


@pytest.fixture
def payouts_api(mock_client):
    """PayoutsAPI instance with mocked client."""
    return PayoutsAPI(mock_client)


@pytest.fixture
def sample_payout_data():
    """Sample payout data for testing."""
    return {
        "id": "payout_123456789",
        "status": "succeeded",
        "amount": {"value": 100.50, "currency": "RUB"},
        "description": "Test payout",
        "payout_destination": {
            "type": "bank_card",
            "card": {
                "first6": "123456",
                "last4": "7890",
                "card_type": "Visa",
                "issuer_country": "RU",
                "issuer_name": "Test Bank",
            },
        },
        "created_at": "2023-01-01T00:00:00.000Z",
        "succeeded_at": "2023-01-01T00:00:01.000Z",
        "test": True,
    }


class TestPayoutsAPI:
    """Test PayoutsAPI class."""

    def test_payouts_api_initialization(self, mock_client):
        """Test PayoutsAPI initialization."""
        api = PayoutsAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_create_payout_minimal(
        self, payouts_api, mock_client, sample_payout_data, sample_payment_amount
    ):
        """Test create_payout with minimal parameters."""
        mock_client._send_request.return_value = sample_payout_data

        params = CreatePayoutParams(amount=sample_payment_amount)
        result = await payouts_api.create_payout(params)

        assert isinstance(result, Payout)
        assert result.id == "payout_123456789"
        assert result.status == PayoutStatus.SUCCEEDED
        assert result.amount.value == pytest.approx(100.50)

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["amount"]["value"] == pytest.approx(100.50)
        assert call_args[1]["json"]["amount"]["currency"] == "RUB"
        assert "Idempotence-Key" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_create_payout_with_all_parameters(
        self,
        payouts_api,
        mock_client,
        sample_payout_data,
        sample_payment_amount,
    ):
        """Test create_payout with all parameters."""
        mock_client._send_request.return_value = sample_payout_data

        card_data = BankCardPayoutCardData(number="5555555555554477")
        destination = BankCardPayoutDestinationData(card=card_data)
        deal = Deal(id="deal_123456789")
        self_employed = SelfEmployed(id="se_123456789")
        receipt_data = PayoutReceiptData(
            service_name="Test service",
            amount=sample_payment_amount,
        )

        params = CreatePayoutParams(
            amount=sample_payment_amount,
            payout_destination_data=destination,
            payout_token="payout_token_123",
            payment_method_id="pm_123456789",
            description="Test payout",
            deal=deal,
            self_employed=self_employed,
            receipt_data=receipt_data,
            personal_data=["pd_123", "pd_456"],
            metadata={"key": "value"},
        )
        result = await payouts_api.create_payout(params)

        assert isinstance(result, Payout)

        # Verify the request was made with all parameters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        json_data = call_args[1]["json"]

        assert json_data["amount"]["value"] == pytest.approx(100.50)
        assert json_data["description"] == "Test payout"
        assert json_data["payout_token"] == "payout_token_123"
        assert json_data["payment_method_id"] == "pm_123456789"
        assert json_data["personal_data"] == ["pd_123", "pd_456"]
        assert json_data["metadata"] == {"key": "value"}
        assert "payout_destination_data" in json_data
        assert "deal" in json_data
        assert "self_employed" in json_data
        assert "receipt_data" in json_data

    @pytest.mark.asyncio
    async def test_create_payout_with_sbp_destination(
        self, payouts_api, mock_client, sample_payout_data, sample_payment_amount
    ):
        """Test create_payout with SBP destination."""
        from aioyookassa.types.params import SbpPayoutDestinationData

        mock_client._send_request.return_value = sample_payout_data

        destination = SbpPayoutDestinationData(
            bank_id="100000000001", phone="79000000000"
        )
        params = CreatePayoutParams(
            amount=sample_payment_amount, payout_destination_data=destination
        )
        result = await payouts_api.create_payout(params)

        assert isinstance(result, Payout)

        # Verify the request was made with SBP destination
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        json_data = call_args[1]["json"]
        assert json_data["payout_destination_data"]["type"] == "sbp"
        assert json_data["payout_destination_data"]["bank_id"] == "100000000001"

    @pytest.mark.asyncio
    async def test_get_payout(self, payouts_api, mock_client, sample_payout_data):
        """Test get_payout."""
        mock_client._send_request.return_value = sample_payout_data

        result = await payouts_api.get_payout("payout_123456789")

        assert isinstance(result, Payout)
        assert result.id == "payout_123456789"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        # Should be called with GetPayout method instance
        assert hasattr(call_args[0][0], "path")

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method_name,method_args,kwargs",
        [
            (
                "create_payout",
                (),
                {
                    "params": CreatePayoutParams(
                        amount=PaymentAmount(value=100.50, currency=Currency.RUB)
                    )
                },
            ),
            ("get_payout", ("payout_123456789",), {}),
        ],
    )
    async def test_api_methods_handle_errors(
        self, payouts_api, mock_client, method_name, method_args, kwargs
    ):
        """Test API methods handle errors."""
        from aioyookassa.exceptions import APIError

        mock_client._send_request.side_effect = APIError("API Error")

        method = getattr(payouts_api, method_name)
        with pytest.raises(APIError):
            await method(*method_args, **kwargs)
