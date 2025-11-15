"""
Tests for PersonalDataAPI client.
"""

from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api.personal_data import PersonalDataAPI
from aioyookassa.types.enum import PersonalDataStatus, PersonalDataType
from aioyookassa.types.params import (
    PayoutStatementRecipientData,
    SbpPayoutRecipientData,
)
from aioyookassa.types.personal_data import PersonalData


@pytest.fixture
def mock_client():
    """Mock BaseAPIClient for testing."""
    client = MagicMock(spec=BaseAPIClient)
    client._send_request = AsyncMock()
    return client


@pytest.fixture
def personal_data_api(mock_client):
    """PersonalDataAPI instance with mocked client."""
    return PersonalDataAPI(mock_client)


@pytest.fixture
def sample_personal_data_sbp():
    """Sample SBP personal data for testing."""
    return {
        "id": "pd_123456789",
        "type": "sbp_payout_recipient",
        "status": "waiting_for_operation",
        "created_at": "2023-01-01T00:00:00.000Z",
        "metadata": {"key": "value"},
    }


@pytest.fixture
def sample_personal_data_statement():
    """Sample statement personal data for testing."""
    return {
        "id": "pd_987654321",
        "type": "payout_statement_recipient",
        "status": "active",
        "created_at": "2023-01-01T00:00:00.000Z",
        "expires_at": "2023-02-01T00:00:00.000Z",
        "metadata": {"order_id": "12345"},
    }


class TestPersonalDataAPI:
    """Test PersonalDataAPI class."""

    def test_personal_data_api_initialization(self, mock_client):
        """Test PersonalDataAPI initialization."""
        api = PersonalDataAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_create_personal_data_sbp_type(
        self, personal_data_api, mock_client, sample_personal_data_sbp
    ):
        """Test create_personal_data with SBP type."""
        mock_client._send_request.return_value = sample_personal_data_sbp

        params = SbpPayoutRecipientData(
            last_name="Ivanov",
            first_name="Ivan",
            middle_name="Ivanovich",
        )
        result = await personal_data_api.create_personal_data(params)

        assert isinstance(result, PersonalData)
        assert result.id == "pd_123456789"
        assert result.type == PersonalDataType.SBP_PAYOUT_RECIPIENT
        assert result.status == PersonalDataStatus.WAITING_FOR_OPERATION

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["type"] == "sbp_payout_recipient"
        assert call_args[1]["json"]["last_name"] == "Ivanov"
        assert call_args[1]["json"]["first_name"] == "Ivan"
        assert call_args[1]["json"]["middle_name"] == "Ivanovich"
        assert "Idempotence-Key" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_create_personal_data_statement_type(
        self, personal_data_api, mock_client, sample_personal_data_statement
    ):
        """Test create_personal_data with statement type."""
        mock_client._send_request.return_value = sample_personal_data_statement

        params = PayoutStatementRecipientData(
            last_name="Petrov",
            first_name="Petr",
            middle_name="Petrovich",
            birthdate=date(1990, 1, 15),
        )
        result = await personal_data_api.create_personal_data(params)

        assert isinstance(result, PersonalData)
        assert result.type == PersonalDataType.PAYOUT_STATEMENT_RECIPIENT
        assert result.status == PersonalDataStatus.ACTIVE

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["type"] == "payout_statement_recipient"
        assert call_args[1]["json"]["last_name"] == "Petrov"
        assert call_args[1]["json"]["birthdate"] == "1990-01-15"

    @pytest.mark.asyncio
    async def test_create_personal_data_with_datetime_birthdate(
        self, personal_data_api, mock_client, sample_personal_data_statement
    ):
        """Test create_personal_data with datetime birthdate."""
        mock_client._send_request.return_value = sample_personal_data_statement

        params = PayoutStatementRecipientData(
            last_name="Sidorov",
            first_name="Sidor",
            birthdate=datetime(1990, 1, 15, 12, 30, 0),
        )
        result = await personal_data_api.create_personal_data(params)

        assert isinstance(result, PersonalData)

        # Verify birthdate was converted to ISO format
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["birthdate"] == "1990-01-15T12:30:00"

    @pytest.mark.asyncio
    async def test_create_personal_data_with_string_birthdate(
        self, personal_data_api, mock_client, sample_personal_data_statement
    ):
        """Test create_personal_data with string birthdate."""
        mock_client._send_request.return_value = sample_personal_data_statement

        params = PayoutStatementRecipientData(
            last_name="Kuznetsov",
            first_name="Kuzma",
            birthdate="1990-01-15",
        )
        result = await personal_data_api.create_personal_data(params)

        assert isinstance(result, PersonalData)

        # Verify string birthdate is preserved
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["birthdate"] == "1990-01-15"

    @pytest.mark.asyncio
    async def test_create_personal_data_with_metadata(
        self, personal_data_api, mock_client, sample_personal_data_sbp
    ):
        """Test create_personal_data with metadata."""
        mock_client._send_request.return_value = sample_personal_data_sbp

        params = SbpPayoutRecipientData(
            last_name="Ivanov",
            first_name="Ivan",
            metadata={"order_id": "12345", "customer_id": "67890"},
        )
        result = await personal_data_api.create_personal_data(params)

        assert isinstance(result, PersonalData)

        # Verify metadata is included
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["metadata"] == {
            "order_id": "12345",
            "customer_id": "67890",
        }

    @pytest.mark.asyncio
    async def test_get_personal_data(
        self, personal_data_api, mock_client, sample_personal_data_sbp
    ):
        """Test get_personal_data."""
        mock_client._send_request.return_value = sample_personal_data_sbp

        result = await personal_data_api.get_personal_data("pd_123456789")

        assert isinstance(result, PersonalData)
        assert result.id == "pd_123456789"
        assert result.type == PersonalDataType.SBP_PAYOUT_RECIPIENT

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        # Should be called with GetPersonalData method instance
        assert hasattr(call_args[0][0], "path")

    @pytest.mark.asyncio
    async def test_get_personal_data_with_active_status(
        self, personal_data_api, mock_client, sample_personal_data_statement
    ):
        """Test get_personal_data with ACTIVE status."""
        mock_client._send_request.return_value = sample_personal_data_statement

        result = await personal_data_api.get_personal_data("pd_987654321")

        assert isinstance(result, PersonalData)
        assert result.status == PersonalDataStatus.ACTIVE
        assert result.expires_at is not None

    @pytest.mark.asyncio
    async def test_get_personal_data_with_canceled_status(
        self, personal_data_api, mock_client
    ):
        """Test get_personal_data with CANCELED status."""
        canceled_data = {
            "id": "pd_123456789",
            "type": "sbp_payout_recipient",
            "status": "canceled",
            "created_at": "2023-01-01T00:00:00.000Z",
            "cancellation_details": {
                "party": "yoo_money",
                "reason": "expired_by_timeout",
            },
        }
        mock_client._send_request.return_value = canceled_data

        result = await personal_data_api.get_personal_data("pd_123456789")

        assert isinstance(result, PersonalData)
        assert result.status == PersonalDataStatus.CANCELED
        assert result.cancellation_details is not None
        assert result.cancellation_details.party.value == "yoo_money"
        assert result.cancellation_details.reason.value == "expired_by_timeout"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method_name,method_args,kwargs",
        [
            (
                "create_personal_data",
                (),
                {
                    "params": SbpPayoutRecipientData(
                        last_name="Ivanov", first_name="Ivan"
                    )
                },
            ),
            ("get_personal_data", ("pd_123456789",), {}),
        ],
    )
    async def test_api_methods_handle_errors(
        self, personal_data_api, mock_client, method_name, method_args, kwargs
    ):
        """Test API methods handle errors."""
        from aioyookassa.exceptions import APIError

        mock_client._send_request.side_effect = APIError("API Error")

        method = getattr(personal_data_api, method_name)
        with pytest.raises(APIError):
            await method(*method_args, **kwargs)
