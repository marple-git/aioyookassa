"""
Tests for webhook types.
"""

import pytest

from aioyookassa.types.webhooks import Webhook, WebhooksList


class TestWebhook:
    """Test Webhook model."""

    def test_webhook_creation(self):
        """Test Webhook creation."""
        webhook = Webhook(
            id="wh_123456789",
            event="payment.succeeded",
            url="https://example.com/webhook",
        )
        assert webhook.id == "wh_123456789"
        assert webhook.event == "payment.succeeded"
        assert webhook.url == "https://example.com/webhook"

    def test_webhook_with_different_events(self):
        """Test Webhook with different event values."""
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
            webhook = Webhook(
                id="wh_123456789",
                event=event,
                url="https://example.com/webhook",
            )
            assert webhook.event == event

    def test_webhook_with_different_urls(self):
        """Test Webhook with different URL formats."""
        urls = [
            "https://example.com/webhook",
            "https://api.example.com/v1/webhooks",
            "http://localhost:8000/webhook",
        ]

        for url in urls:
            webhook = Webhook(
                id="wh_123456789",
                event="payment.succeeded",
                url=url,
            )
            assert webhook.url == url


class TestWebhooksList:
    """Test WebhooksList model."""

    def test_webhooks_list_creation_empty(self):
        """Test WebhooksList creation with empty list."""
        webhooks_list = WebhooksList()
        assert webhooks_list.list is None

    def test_webhooks_list_creation_with_webhooks(self):
        """Test WebhooksList creation with webhooks."""
        webhook1 = Webhook(
            id="wh_123456789",
            event="payment.succeeded",
            url="https://example.com/webhook1",
        )
        webhook2 = Webhook(
            id="wh_987654321",
            event="payment.canceled",
            url="https://example.com/webhook2",
        )

        webhooks_list = WebhooksList(items=[webhook1, webhook2])
        assert len(webhooks_list.list) == 2
        assert webhooks_list.list[0].id == "wh_123456789"
        assert webhooks_list.list[1].id == "wh_987654321"

    def test_webhooks_list_with_alias(self):
        """Test WebhooksList with alias 'items'."""
        webhook = Webhook(
            id="wh_123456789",
            event="payment.succeeded",
            url="https://example.com/webhook",
        )

        # Test with alias 'items'
        webhooks_list = WebhooksList(items=[webhook])
        assert len(webhooks_list.list) == 1
        assert webhooks_list.list[0].id == "wh_123456789"

    def test_webhooks_list_single_webhook(self):
        """Test WebhooksList with single webhook."""
        webhook = Webhook(
            id="wh_123456789",
            event="refund.succeeded",
            url="https://example.com/refund-webhook",
        )

        webhooks_list = WebhooksList(items=[webhook])
        assert len(webhooks_list.list) == 1
        assert webhooks_list.list[0].event == "refund.succeeded"
