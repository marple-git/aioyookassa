"""
Tests for WebhookNotification type.
"""

import pytest

from aioyookassa.types.webhook_notification import WebhookNotification


class TestWebhookNotification:
    """Test WebhookNotification model."""

    def test_webhook_notification_creation(self):
        """Test WebhookNotification creation with valid data."""
        data = {
            "type": "notification",
            "event": "payment.succeeded",
            "object": {"id": "payment_123", "status": "succeeded"},
        }
        notification = WebhookNotification(**data)

        assert notification.type == "notification"
        assert notification.event == "payment.succeeded"
        assert notification.object == {"id": "payment_123", "status": "succeeded"}

    def test_webhook_notification_invalid_type(self):
        """Test WebhookNotification with invalid type."""
        data = {
            "type": "invalid",
            "event": "payment.succeeded",
            "object": {},
        }

        with pytest.raises(Exception):  # Pydantic validation error
            WebhookNotification(**data)

    def test_webhook_notification_missing_fields(self):
        """Test WebhookNotification with missing required fields."""
        data = {
            "type": "notification",
            # Missing event and object
        }

        with pytest.raises(Exception):  # Pydantic validation error
            WebhookNotification(**data)

    def test_webhook_notification_different_events(self):
        """Test WebhookNotification with different event types."""
        events = [
            "payment.succeeded",
            "payment.canceled",
            "refund.succeeded",
            "payout.succeeded",
            "deal.closed",
        ]

        for event in events:
            data = {
                "type": "notification",
                "event": event,
                "object": {"id": "test_123"},
            }
            notification = WebhookNotification(**data)
            assert notification.event == event
