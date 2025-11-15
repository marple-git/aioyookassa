"""
Tests for SelfEmployedAPI client.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api.self_employed import SelfEmployedAPI
from aioyookassa.types.enum import SelfEmployedStatus
from aioyookassa.types.params import (
    CreateSelfEmployedParams,
    SelfEmployedConfirmationData,
)
from aioyookassa.types.payout import SelfEmployed, SelfEmployedConfirmation


@pytest.fixture
def mock_client():
    """Mock BaseAPIClient for testing."""
    client = MagicMock(spec=BaseAPIClient)
    client._send_request = AsyncMock()
    return client


@pytest.fixture
def self_employed_api(mock_client):
    """SelfEmployedAPI instance with mocked client."""
    return SelfEmployedAPI(mock_client)


@pytest.fixture
def sample_self_employed_data():
    """Sample self-employed data for testing."""
    return {
        "id": "se_123456789",
        "status": "confirmed",
        "created_at": "2023-01-01T00:00:00.000Z",
        "itn": "123456789012",
        "phone": "79000000000",
        "confirmation": {
            "type": "redirect",
            "confirmation_url": "https://example.com/confirm",
        },
        "test": True,
    }


class TestSelfEmployedAPI:
    """Test SelfEmployedAPI class."""

    def test_self_employed_api_initialization(self, mock_client):
        """Test SelfEmployedAPI initialization."""
        api = SelfEmployedAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_create_self_employed_with_itn(
        self, self_employed_api, mock_client, sample_self_employed_data
    ):
        """Test create_self_employed with ITN."""
        mock_client._send_request.return_value = sample_self_employed_data

        params = CreateSelfEmployedParams(itn="123456789012")
        result = await self_employed_api.create_self_employed(params)

        assert isinstance(result, SelfEmployed)
        assert result.id == "se_123456789"
        assert result.status == SelfEmployedStatus.CONFIRMED
        assert result.itn == "123456789012"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["itn"] == "123456789012"
        assert "Idempotence-Key" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_create_self_employed_with_phone(
        self, self_employed_api, mock_client, sample_self_employed_data
    ):
        """Test create_self_employed with phone."""
        mock_client._send_request.return_value = sample_self_employed_data

        params = CreateSelfEmployedParams(phone="79000000000")
        result = await self_employed_api.create_self_employed(params)

        assert isinstance(result, SelfEmployed)
        assert result.phone == "79000000000"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["phone"] == "79000000000"

    @pytest.mark.asyncio
    async def test_create_self_employed_with_all_parameters(
        self, self_employed_api, mock_client, sample_self_employed_data
    ):
        """Test create_self_employed with all parameters."""
        mock_client._send_request.return_value = sample_self_employed_data

        confirmation = SelfEmployedConfirmationData(
            confirmation_url="https://example.com/confirm"
        )

        params = CreateSelfEmployedParams(
            itn="123456789012",
            phone="79000000000",
            confirmation=confirmation,
        )
        result = await self_employed_api.create_self_employed(params)

        assert isinstance(result, SelfEmployed)

        # Verify the request was made with all parameters
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        json_data = call_args[1]["json"]

        assert json_data["itn"] == "123456789012"
        assert json_data["phone"] == "79000000000"
        assert json_data["confirmation"]["type"] == "redirect"
        assert (
            json_data["confirmation"]["confirmation_url"]
            == "https://example.com/confirm"
        )

    @pytest.mark.asyncio
    async def test_get_self_employed(
        self, self_employed_api, mock_client, sample_self_employed_data
    ):
        """Test get_self_employed."""
        mock_client._send_request.return_value = sample_self_employed_data

        result = await self_employed_api.get_self_employed("se_123456789")

        assert isinstance(result, SelfEmployed)
        assert result.id == "se_123456789"
        assert result.status == SelfEmployedStatus.CONFIRMED

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        # Should be called with GetSelfEmployed method instance
        assert hasattr(call_args[0][0], "path")

    @pytest.mark.asyncio
    async def test_get_self_employed_with_pending_status(
        self, self_employed_api, mock_client
    ):
        """Test get_self_employed with pending status."""
        pending_data = {
            "id": "se_123456789",
            "status": "pending",
            "created_at": "2023-01-01T00:00:00.000Z",
            "confirmation": {
                "type": "redirect",
                "confirmation_url": "https://example.com/confirm",
            },
            "test": False,
        }
        mock_client._send_request.return_value = pending_data

        result = await self_employed_api.get_self_employed("se_123456789")

        assert isinstance(result, SelfEmployed)
        assert result.status == SelfEmployedStatus.PENDING
        assert result.confirmation is not None
        assert result.confirmation.confirmation_url == "https://example.com/confirm"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method_name,method_args,kwargs",
        [
            (
                "create_self_employed",
                (),
                {"params": CreateSelfEmployedParams(itn="123456789012")},
            ),
            ("get_self_employed", ("se_123456789",), {}),
        ],
    )
    async def test_api_methods_handle_errors(
        self, self_employed_api, mock_client, method_name, method_args, kwargs
    ):
        """Test API methods handle errors."""
        from aioyookassa.exceptions import APIError

        mock_client._send_request.side_effect = APIError("API Error")

        method = getattr(self_employed_api, method_name)
        with pytest.raises(APIError):
            await method(*method_args, **kwargs)
