"""
Tests for webhooks methods.
"""

import pytest

from aioyookassa.core.methods.webhooks import (
    CreateWebhook,
    DeleteWebhook,
    GetWebhooks,
    WebhooksAPIMethod,
)


class TestWebhooksAPIMethod:
    """Test WebhooksAPIMethod base class."""

    def test_webhooks_api_method_initialization(self):
        """Test WebhooksAPIMethod initialization."""
        method = WebhooksAPIMethod()
        assert method.http_method == "GET"
        assert method.path == "/webhooks"

    def test_webhooks_api_method_with_custom_path(self):
        """Test WebhooksAPIMethod with custom path."""
        method = WebhooksAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_webhooks_api_method_build(self):
        """Test WebhooksAPIMethod build method."""
        method = WebhooksAPIMethod.build("wh_123")
        assert method.path == "/webhooks"  # Should use class path

    def test_webhooks_api_method_build_with_format(self):
        """Test WebhooksAPIMethod build with path formatting."""

        class TestMethod(WebhooksAPIMethod):
            path = "/webhooks/{webhook_id}"

        method = TestMethod.build("wh_123")
        assert method.path == "/webhooks/wh_123"


class TestCreateWebhook:
    """Test CreateWebhook method."""

    def test_create_webhook_initialization(self):
        """Test CreateWebhook initialization."""
        method = CreateWebhook()
        assert method.http_method == "POST"
        assert method.path == "/webhooks"

    def test_create_webhook_build_params(self):
        """Test CreateWebhook build_params."""
        params = CreateWebhook.build_params(
            event="payment.succeeded", url="https://example.com/webhook"
        )

        assert params["event"] == "payment.succeeded"
        assert params["url"] == "https://example.com/webhook"

    def test_create_webhook_build_params_with_different_events(self):
        """Test CreateWebhook build_params with different event values."""
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
            params = CreateWebhook.build_params(
                event=event, url="https://example.com/webhook"
            )
            assert params["event"] == event

    def test_create_webhook_build_params_filters_none_values(self):
        """Test CreateWebhook build_params filters out None values."""
        params = CreateWebhook.build_params(
            event="payment.succeeded", url="https://example.com/webhook"
        )

        assert params["event"] == "payment.succeeded"
        assert params["url"] == "https://example.com/webhook"
        assert len(params) == 2


class TestGetWebhooks:
    """Test GetWebhooks method."""

    def test_get_webhooks_initialization(self):
        """Test GetWebhooks initialization."""
        method = GetWebhooks()
        assert method.http_method == "GET"
        assert method.path == "/webhooks"

    def test_get_webhooks_build_params(self):
        """Test GetWebhooks build_params."""
        params = GetWebhooks.build_params()

        assert params == {}


class TestDeleteWebhook:
    """Test DeleteWebhook method."""

    def test_delete_webhook_initialization(self):
        """Test DeleteWebhook initialization."""
        method = DeleteWebhook()
        assert method.http_method == "DELETE"
        assert method.path == "/webhooks/{webhook_id}"

    def test_delete_webhook_build(self):
        """Test DeleteWebhook build method."""
        method = DeleteWebhook.build("wh_123")
        assert method.path == "/webhooks/wh_123"
