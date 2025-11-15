"""
Tests for SbpBanksAPI client.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api.sbp_banks import SbpBanksAPI
from aioyookassa.types.sbp_banks import SbpBanksList, SbpParticipantBank


@pytest.fixture
def mock_client():
    """Mock BaseAPIClient for testing."""
    client = MagicMock(spec=BaseAPIClient)
    client._send_request = AsyncMock()
    return client


@pytest.fixture
def sbp_banks_api(mock_client):
    """SbpBanksAPI instance with mocked client."""
    return SbpBanksAPI(mock_client)


@pytest.fixture
def sample_sbp_banks_data():
    """Sample SBP banks data for testing."""
    return {
        "items": [
            {
                "bank_id": "100000000001",
                "name": "Test Bank 1",
                "bic": "044525225",
            },
            {
                "bank_id": "100000000002",
                "name": "Test Bank 2",
                "bic": "044525226",
            },
        ]
    }


class TestSbpBanksAPI:
    """Test SbpBanksAPI class."""

    def test_sbp_banks_api_initialization(self, mock_client):
        """Test SbpBanksAPI initialization."""
        api = SbpBanksAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_get_sbp_banks(
        self, sbp_banks_api, mock_client, sample_sbp_banks_data
    ):
        """Test get_sbp_banks."""
        mock_client._send_request.return_value = sample_sbp_banks_data

        result = await sbp_banks_api.get_sbp_banks()

        assert isinstance(result, SbpBanksList)
        assert len(result.list) == 2
        assert result.list[0].bank_id == "100000000001"
        assert result.list[0].name == "Test Bank 1"
        assert result.list[0].bic == "044525225"
        assert result.list[1].bank_id == "100000000002"
        assert result.list[1].name == "Test Bank 2"
        assert result.list[1].bic == "044525226"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        # Should be called with GetSbpBanks method instance
        assert hasattr(call_args[0][0], "path")
        # Should have empty params
        assert call_args[1].get("params") == {}

    @pytest.mark.asyncio
    async def test_get_sbp_banks_empty_list(self, sbp_banks_api, mock_client):
        """Test get_sbp_banks with empty list."""
        empty_data = {"items": []}
        mock_client._send_request.return_value = empty_data

        result = await sbp_banks_api.get_sbp_banks()

        assert isinstance(result, SbpBanksList)
        assert len(result.list) == 0

    @pytest.mark.asyncio
    async def test_get_sbp_banks_single_bank(self, sbp_banks_api, mock_client):
        """Test get_sbp_banks with single bank."""
        single_bank_data = {
            "items": [
                {
                    "bank_id": "100000000001",
                    "name": "Single Bank",
                    "bic": "044525225",
                }
            ]
        }
        mock_client._send_request.return_value = single_bank_data

        result = await sbp_banks_api.get_sbp_banks()

        assert isinstance(result, SbpBanksList)
        assert len(result.list) == 1
        assert result.list[0].bank_id == "100000000001"
        assert result.list[0].name == "Single Bank"
        assert result.list[0].bic == "044525225"

    @pytest.mark.asyncio
    async def test_get_sbp_banks_handle_errors(self, sbp_banks_api, mock_client):
        """Test get_sbp_banks handles errors."""
        from aioyookassa.exceptions import APIError

        mock_client._send_request.side_effect = APIError("API Error")

        with pytest.raises(APIError):
            await sbp_banks_api.get_sbp_banks()
