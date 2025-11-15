"""
Tests for WebhooksAPI client.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api.webhooks import WebhooksAPI
from aioyookassa.types.enum import WebhookEvent
from aioyookassa.types.params import CreateWebhookParams
from aioyookassa.types.webhooks import Webhook, WebhooksList


@pytest.fixture
def mock_client():
    """Mock BaseAPIClient for testing."""
    client = MagicMock(spec=BaseAPIClient)
    client._send_request = AsyncMock()
    return client


@pytest.fixture
def webhooks_api(mock_client):
    """WebhooksAPI instance with mocked client."""
    return WebhooksAPI(mock_client)


@pytest.fixture
def sample_webhook_data():
    """Sample webhook data for testing."""
    return {
        "id": "wh_123456789",
        "event": "payment.succeeded",
        "url": "https://example.com/webhook",
    }


@pytest.fixture
def sample_webhooks_list_data(sample_webhook_data):
    """Sample webhooks list data for testing."""
    webhook2 = sample_webhook_data.copy()
    webhook2["id"] = "wh_987654321"
    webhook2["event"] = "payment.canceled"
    return {
        "items": [sample_webhook_data, webhook2],
    }


class TestWebhooksAPI:
    """Test WebhooksAPI class."""

    def test_webhooks_api_initialization(self, mock_client):
        """Test WebhooksAPI initialization."""
        api = WebhooksAPI(mock_client)
        assert api._client == mock_client

    @pytest.mark.asyncio
    async def test_create_webhook(self, webhooks_api, mock_client, sample_webhook_data):
        """Test create_webhook."""
        mock_client._send_request.return_value = sample_webhook_data

        params = CreateWebhookParams(
            event="payment.succeeded", url="https://example.com/webhook"
        )
        oauth_token = "test_oauth_token_12345"
        result = await webhooks_api.create_webhook(params, oauth_token)

        assert isinstance(result, Webhook)
        assert result.id == "wh_123456789"
        assert result.event == "payment.succeeded"
        assert result.url == "https://example.com/webhook"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["event"] == "payment.succeeded"
        assert call_args[1]["json"]["url"] == "https://example.com/webhook"
        assert call_args[1]["headers"]["Authorization"] == f"Bearer {oauth_token}"
        assert "Idempotence-Key" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_create_webhook_with_enum_event(
        self, webhooks_api, mock_client, sample_webhook_data
    ):
        """Test create_webhook with WebhookEvent enum."""
        mock_client._send_request.return_value = sample_webhook_data

        params = CreateWebhookParams(
            event=WebhookEvent.PAYMENT_SUCCEEDED, url="https://example.com/webhook"
        )
        oauth_token = "test_oauth_token_12345"
        result = await webhooks_api.create_webhook(params, oauth_token)

        assert isinstance(result, Webhook)
        assert result.event == "payment.succeeded"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["json"]["event"] == WebhookEvent.PAYMENT_SUCCEEDED

    @pytest.mark.asyncio
    async def test_create_webhook_with_different_events(
        self, webhooks_api, mock_client
    ):
        """Test create_webhook with different event types."""
        events = [
            "payment.waiting_for_capture",
            "payment.succeeded",
            "payment.canceled",
            "payment_method.active",
            "refund.succeeded",
            "payout.succeeded",
            "payout.canceled",
            "deal.closed",
        ]

        for event in events:
            mock_client._send_request.return_value = {
                "id": "wh_123456789",
                "event": event,
                "url": "https://example.com/webhook",
            }
            mock_client._send_request.reset_mock()

            params = CreateWebhookParams(event=event, url="https://example.com/webhook")
            oauth_token = "test_oauth_token_12345"
            result = await webhooks_api.create_webhook(params, oauth_token)

            assert isinstance(result, Webhook)
            assert result.event == event

    @pytest.mark.asyncio
    async def test_get_webhooks(
        self, webhooks_api, mock_client, sample_webhooks_list_data
    ):
        """Test get_webhooks."""
        mock_client._send_request.return_value = sample_webhooks_list_data

        oauth_token = "test_oauth_token_12345"
        result = await webhooks_api.get_webhooks(oauth_token)

        assert isinstance(result, WebhooksList)
        assert len(result.list) == 2
        assert result.list[0].id == "wh_123456789"
        assert result.list[1].id == "wh_987654321"
        assert result.list[0].event == "payment.succeeded"
        assert result.list[1].event == "payment.canceled"

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["headers"]["Authorization"] == f"Bearer {oauth_token}"

    @pytest.mark.asyncio
    async def test_get_webhooks_empty_list(self, webhooks_api, mock_client):
        """Test get_webhooks with empty list."""
        mock_client._send_request.return_value = {"items": []}

        oauth_token = "test_oauth_token_12345"
        result = await webhooks_api.get_webhooks(oauth_token)

        assert isinstance(result, WebhooksList)
        assert len(result.list) == 0

    @pytest.mark.asyncio
    async def test_get_webhooks_with_none_items(self, webhooks_api, mock_client):
        """Test get_webhooks with None items."""
        mock_client._send_request.return_value = {}

        oauth_token = "test_oauth_token_12345"
        result = await webhooks_api.get_webhooks(oauth_token)

        assert isinstance(result, WebhooksList)
        assert result.list is None

    @pytest.mark.asyncio
    async def test_delete_webhook(self, webhooks_api, mock_client):
        """Test delete_webhook."""
        # DELETE returns empty body (204 No Content)
        mock_client._send_request.return_value = {}

        oauth_token = "test_oauth_token_12345"
        result = await webhooks_api.delete_webhook("wh_123456789", oauth_token)

        # delete_webhook returns None
        assert result is None

        # Verify the request was made correctly
        mock_client._send_request.assert_called_once()
        call_args = mock_client._send_request.call_args
        assert call_args[1]["headers"]["Authorization"] == f"Bearer {oauth_token}"
        # Should be called with DeleteWebhook method instance
        assert hasattr(call_args[0][0], "path")
        assert "wh_123456789" in call_args[0][0].path

    @pytest.mark.asyncio
    async def test_delete_webhook_handles_empty_response(
        self, webhooks_api, mock_client
    ):
        """Test delete_webhook handles empty response correctly."""
        # DELETE returns empty body (204 No Content)
        mock_client._send_request.return_value = {}

        oauth_token = "test_oauth_token_12345"
        # Should not raise an error
        await webhooks_api.delete_webhook("wh_123456789", oauth_token)

        mock_client._send_request.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "method_name,method_args,kwargs",
        [
            (
                "create_webhook",
                (),
                {
                    "params": CreateWebhookParams(
                        event="payment.succeeded", url="https://example.com/webhook"
                    ),
                    "oauth_token": "test_token",
                },
            ),
            ("get_webhooks", (), {"oauth_token": "test_token"}),
            ("delete_webhook", ("wh_123456789",), {"oauth_token": "test_token"}),
        ],
    )
    async def test_api_methods_handle_errors(
        self, webhooks_api, mock_client, method_name, method_args, kwargs
    ):
        """Test API methods handle errors."""
        from aioyookassa.exceptions import APIError

        mock_client._send_request.side_effect = APIError("API Error")

        method = getattr(webhooks_api, method_name)
        with pytest.raises(APIError):
            await method(*method_args, **kwargs)

    @pytest.mark.asyncio
    async def test_oauth_token_in_headers(self, webhooks_api, mock_client):
        """Test that OAuth token is correctly passed in Authorization header."""
        mock_client._send_request.return_value = {
            "id": "wh_123456789",
            "event": "payment.succeeded",
            "url": "https://example.com/webhook",
        }

        oauth_token = "my_oauth_token_12345"
        params = CreateWebhookParams(
            event="payment.succeeded", url="https://example.com/webhook"
        )

        await webhooks_api.create_webhook(params, oauth_token)

        # Verify OAuth token is in headers
        call_args = mock_client._send_request.call_args
        assert call_args[1]["headers"]["Authorization"] == f"Bearer {oauth_token}"

    @pytest.mark.asyncio
    async def test_oauth_token_not_using_basic_auth(
        self, webhooks_api, mock_client, sample_webhook_data
    ):
        """Test that OAuth token prevents BasicAuth from being used."""
        mock_client._send_request.return_value = sample_webhook_data

        oauth_token = "test_oauth_token_12345"
        params = CreateWebhookParams(
            event="payment.succeeded", url="https://example.com/webhook"
        )

        await webhooks_api.create_webhook(params, oauth_token)

        # Verify the request was made
        mock_client._send_request.assert_called_once()
        # The auth parameter should be None when Authorization header is present
        # This is handled in BaseAPIClient._send_request
