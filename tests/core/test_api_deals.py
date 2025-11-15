"""
Tests for DealsAPI client.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api.deals import DealsAPI
from aioyookassa.types.deals import Deal, DealsList
from aioyookassa.types.enum import Currency, DealStatus, FeeMoment
from aioyookassa.types.params import CreateDealParams, GetDealsParams
from aioyookassa.types.payment import PaymentAmount


@pytest.fixture
def mock_client():
    """Mock BaseAPIClient for testing."""
    client = MagicMock(spec=BaseAPIClient)
    client._send_request = AsyncMock()
    return client


@pytest.fixture
def deals_api(mock_client):
    """DealsAPI instance with mocked client."""
    return DealsAPI(mock_client)


@pytest.fixture
def sample_deal_data():
    """Sample deal data for testing."""
    return {
        "id": "deal_123456789",
        "type": "safe_deal",
        "fee_moment": "payment_succeeded",
        "description": "Test deal",
        "balance": {"value": 1000.00, "currency": "RUB"},
        "payout_balance": {"value": 950.00, "currency": "RUB"},
        "status": "opened",
        "created_at": "2023-01-01T00:00:00.000Z",
        "expires_at": "2023-04-01T00:00:00.000Z",
        "metadata": {"order_id": "12345"},
        "test": True,
    }


@pytest.fixture
def sample_deals_list_data(sample_deal_data):
    """Sample deals list data for testing."""
    deal2 = sample_deal_data.copy()
    deal2["id"] = "deal_987654321"
    deal2["status"] = "closed"
    return {
        "items": [sample_deal_data, deal2],
        "next_cursor": "next_cursor_123",
    }


class TestDealsAPI:
    """Test DealsAPI class."""

    def test_deals_api_initialization(self, mock_client):
        """Test DealsAPI initialization."""
        api = DealsAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_create_deal_minimal(self, deals_api, mock_client, sample_deal_data):
        """Test create_deal with minimal parameters."""
        mock_client._send_request.return_value = sample_deal_data

        params = CreateDealParams(fee_moment=FeeMoment.PAYMENT_SUCCEEDED)
        result = await deals_api.create_deal(params)

        assert isinstance(result, Deal)
        assert result.id == "deal_123456789"
        assert result.type == "safe_deal"
        assert result.fee_moment == FeeMoment.PAYMENT_SUCCEEDED
        assert result.status == DealStatus.OPENED

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["type"] == "safe_deal"
        assert call_args[1]["json"]["fee_moment"] == FeeMoment.PAYMENT_SUCCEEDED
        assert "Idempotence-Key" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_create_deal_with_all_parameters(
        self, deals_api, mock_client, sample_deal_data
    ):
        """Test create_deal with all parameters."""
        mock_client._send_request.return_value = sample_deal_data

        params = CreateDealParams(
            fee_moment=FeeMoment.DEAL_CLOSED,
            description="Test deal description",
            metadata={"order_id": "12345", "customer_id": "67890"},
        )
        result = await deals_api.create_deal(params)

        assert isinstance(result, Deal)

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["fee_moment"] == FeeMoment.DEAL_CLOSED
        assert call_args[1]["json"]["description"] == "Test deal description"
        assert call_args[1]["json"]["metadata"] == {
            "order_id": "12345",
            "customer_id": "67890",
        }

    @pytest.mark.asyncio
    async def test_get_deals_minimal(
        self, deals_api, mock_client, sample_deals_list_data
    ):
        """Test get_deals with minimal parameters."""
        mock_client._send_request.return_value = sample_deals_list_data

        result = await deals_api.get_deals()

        assert isinstance(result, DealsList)
        assert len(result.list) == 2
        assert result.list[0].id == "deal_123456789"
        assert result.list[1].id == "deal_987654321"
        assert result.next_cursor == "next_cursor_123"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["params"] is not None

    @pytest.mark.asyncio
    async def test_get_deals_with_filters(
        self, deals_api, mock_client, sample_deals_list_data
    ):
        """Test get_deals with filters."""
        mock_client._send_request.return_value = sample_deals_list_data

        created_at_gte = datetime(2023, 1, 1, 12, 0, 0)
        expires_at_lte = datetime(2023, 4, 30, 23, 59, 59)

        params = GetDealsParams(
            created_at_gte=created_at_gte,
            expires_at_lte=expires_at_lte,
            status=DealStatus.OPENED,
            full_text_search="test",
            limit=50,
            cursor="cursor_123",
        )
        result = await deals_api.get_deals(params)

        assert isinstance(result, DealsList)

        # Verify the request was made with filters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        request_params = call_args[1]["params"]

        assert "created_at.gte" in request_params
        assert "expires_at.lte" in request_params
        assert request_params["status"] == DealStatus.OPENED
        assert request_params["full_text_search"] == "test"
        assert request_params["limit"] == 50
        assert request_params["cursor"] == "cursor_123"

    @pytest.mark.asyncio
    async def test_get_deals_with_all_datetime_filters(
        self, deals_api, mock_client, sample_deals_list_data
    ):
        """Test get_deals with all datetime filters."""
        mock_client._send_request.return_value = sample_deals_list_data

        created_at_gte = datetime(2023, 1, 1, 12, 0, 0)
        created_at_gt = datetime(2023, 1, 2, 12, 0, 0)
        created_at_lte = datetime(2023, 1, 31, 23, 59, 59)
        created_at_lt = datetime(2023, 2, 1, 0, 0, 0)
        expires_at_gte = datetime(2023, 4, 1, 12, 0, 0)
        expires_at_gt = datetime(2023, 4, 2, 12, 0, 0)
        expires_at_lte = datetime(2023, 4, 30, 23, 59, 59)
        expires_at_lt = datetime(2023, 5, 1, 0, 0, 0)

        params = GetDealsParams(
            created_at_gte=created_at_gte,
            created_at_gt=created_at_gt,
            created_at_lte=created_at_lte,
            created_at_lt=created_at_lt,
            expires_at_gte=expires_at_gte,
            expires_at_gt=expires_at_gt,
            expires_at_lte=expires_at_lte,
            expires_at_lt=expires_at_lt,
        )
        result = await deals_api.get_deals(params)

        assert isinstance(result, DealsList)

        # Verify all datetime filters are converted correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        request_params = call_args[1]["params"]

        assert "created_at.gte" in request_params
        assert "created_at.gt" in request_params
        assert "created_at.lte" in request_params
        assert "created_at.lt" in request_params
        assert "expires_at.gte" in request_params
        assert "expires_at.gt" in request_params
        assert "expires_at.lte" in request_params
        assert "expires_at.lt" in request_params

    @pytest.mark.asyncio
    async def test_get_deal(self, deals_api, mock_client, sample_deal_data):
        """Test get_deal."""
        mock_client._send_request.return_value = sample_deal_data

        result = await deals_api.get_deal("deal_123456789")

        assert isinstance(result, Deal)
        assert result.id == "deal_123456789"
        assert result.type == "safe_deal"
        assert result.fee_moment == FeeMoment.PAYMENT_SUCCEEDED
        assert result.status == DealStatus.OPENED
        assert result.balance.value == pytest.approx(1000.00)
        assert result.payout_balance.value == pytest.approx(950.00)

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        # Should be called with GetDeal method instance
        assert hasattr(call_args[0][0], "path")

    @pytest.mark.asyncio
    async def test_get_deal_with_closed_status(self, deals_api, mock_client):
        """Test get_deal with CLOSED status."""
        closed_deal_data = {
            "id": "deal_123456789",
            "type": "safe_deal",
            "fee_moment": "deal_closed",
            "balance": {"value": 1000.00, "currency": "RUB"},
            "payout_balance": {"value": 950.00, "currency": "RUB"},
            "status": "closed",
            "created_at": "2023-01-01T00:00:00.000Z",
            "expires_at": "2023-04-01T00:00:00.000Z",
            "test": True,
        }
        mock_client._send_request.return_value = closed_deal_data

        result = await deals_api.get_deal("deal_123456789")

        assert isinstance(result, Deal)
        assert result.status == DealStatus.CLOSED
        assert result.fee_moment == FeeMoment.DEAL_CLOSED

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method_name,method_args,kwargs",
        [
            (
                "create_deal",
                (),
                {"params": CreateDealParams(fee_moment=FeeMoment.PAYMENT_SUCCEEDED)},
            ),
            ("get_deals", (), {}),
            ("get_deal", ("deal_123456789",), {}),
        ],
    )
    async def test_api_methods_handle_errors(
        self, deals_api, mock_client, method_name, method_args, kwargs
    ):
        """Test API methods handle errors."""
        from aioyookassa.exceptions import APIError

        mock_client._send_request.side_effect = APIError("API Error")

        method = getattr(deals_api, method_name)
        with pytest.raises(APIError):
            await method(*method_args, **kwargs)
