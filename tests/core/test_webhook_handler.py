"""
Tests for WebhookHandler.
"""

import pytest

from aioyookassa.core.webhook_handler import WebhookHandler
from aioyookassa.core.webhook_validator import WebhookIPValidator
from aioyookassa.exceptions.webhooks import InvalidWebhookDataError
from aioyookassa.types.enum import WebhookEvent
from aioyookassa.types.payment import Payment
from aioyookassa.types.refund import Refund
from aioyookassa.types.webhook_notification import WebhookNotification


@pytest.fixture
def handler():
    """Create WebhookHandler instance for testing."""
    return WebhookHandler()


@pytest.fixture
def sample_payment_notification():
    """Sample payment notification data."""
    return {
        "type": "notification",
        "event": "payment.succeeded",
        "object": {
            "id": "payment_123",
            "status": "succeeded",
            "amount": {"value": "100.00", "currency": "RUB"},
            "recipient": {"account_id": "123", "gateway_id": "456"},
            "created_at": "2023-01-01T00:00:00.000Z",
            "test": False,
            "paid": True,
            "refundable": True,
        },
    }


@pytest.fixture
def sample_refund_notification():
    """Sample refund notification data."""
    return {
        "type": "notification",
        "event": "refund.succeeded",
        "object": {
            "id": "refund_123",
            "payment_id": "payment_123",
            "status": "succeeded",
            "amount": {"value": "50.00", "currency": "RUB"},
            "created_at": "2023-01-01T00:00:00.000Z",
        },
    }


class TestWebhookHandler:
    """Test WebhookHandler."""

    def test_handler_initialization(self):
        """Test handler initialization."""
        handler = WebhookHandler()
        assert handler.validator is not None
        assert isinstance(handler.validator, WebhookIPValidator)

    def test_handler_with_custom_validator(self):
        """Test handler with custom validator."""
        validator = WebhookIPValidator(allowed_ips=["192.168.1.1"])
        handler = WebhookHandler(validator=validator)
        assert handler.validator == validator

    def test_parse_notification(self, handler, sample_payment_notification):
        """Test parsing notification."""
        notification = handler.parse_notification(sample_payment_notification)

        assert isinstance(notification, WebhookNotification)
        assert notification.type == "notification"
        assert notification.event == "payment.succeeded"

    def test_parse_notification_invalid(self, handler):
        """Test parsing invalid notification."""
        invalid_data = {"type": "invalid"}

        with pytest.raises(InvalidWebhookDataError):
            handler.parse_notification(invalid_data)

    @pytest.mark.asyncio
    async def test_handle_notification_payment(
        self, handler, sample_payment_notification
    ):
        """Test handling payment notification."""
        notification = handler.parse_notification(sample_payment_notification)
        event_object = await handler.handle_notification(notification)

        assert isinstance(event_object, Payment)
        assert event_object.id == "payment_123"
        assert event_object.status.value == "succeeded"

    @pytest.mark.asyncio
    async def test_handle_notification_refund(
        self, handler, sample_refund_notification
    ):
        """Test handling refund notification."""
        notification = handler.parse_notification(sample_refund_notification)
        event_object = await handler.handle_notification(notification)

        assert isinstance(event_object, Refund)
        assert event_object.id == "refund_123"
        assert event_object.payment_id == "payment_123"

    def test_register_callback_single_event(self, handler):
        """Test registering callback for single event."""
        callback_called = False

        @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
        def callback(payment: Payment):
            nonlocal callback_called
            callback_called = True

        assert str(WebhookEvent.PAYMENT_SUCCEEDED) in handler.callbacks

    def test_register_callback_multiple_events(self, handler):
        """Test registering callback for multiple events."""
        callback_called_count = 0

        @handler.register_callback(
            [
                WebhookEvent.PAYMENT_SUCCEEDED,
                WebhookEvent.PAYMENT_CANCELED,
            ]
        )
        def callback(payment: Payment):
            nonlocal callback_called_count
            callback_called_count += 1

        assert str(WebhookEvent.PAYMENT_SUCCEEDED) in handler.callbacks
        assert str(WebhookEvent.PAYMENT_CANCELED) in handler.callbacks

    def test_register_callback_pattern(self, handler):
        """Test registering callback with pattern."""

        @handler.register_callback("payment.*")
        def callback(payment: Payment):
            # Empty callback - this test only verifies registration, not execution
            pass

        assert len(handler.pattern_callbacks) == 1

    def test_add_callback(self, handler):
        """Test adding callback without decorator."""

        def callback(payment: Payment):
            # Empty callback - this test only verifies registration, not execution
            pass

        handler.add_callback(WebhookEvent.PAYMENT_SUCCEEDED, callback)
        assert str(WebhookEvent.PAYMENT_SUCCEEDED) in handler.callbacks

    @pytest.mark.asyncio
    async def test_callback_invocation(self, handler, sample_payment_notification):
        """Test that registered callback is called."""
        callback_called = False
        received_payment = None

        @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
        def callback(payment: Payment):
            nonlocal callback_called, received_payment
            callback_called = True
            received_payment = payment

        notification = handler.parse_notification(sample_payment_notification)
        await handler.handle_notification(notification)

        assert callback_called is True
        assert isinstance(received_payment, Payment)
        assert received_payment.id == "payment_123"

    @pytest.mark.asyncio
    async def test_async_callback(self, handler, sample_payment_notification):
        """Test async callback invocation."""
        callback_called = False

        @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
        async def callback(payment: Payment):
            nonlocal callback_called
            callback_called = True

        notification = handler.parse_notification(sample_payment_notification)
        await handler.handle_notification(notification)

        assert callback_called is True

    @pytest.mark.asyncio
    async def test_pattern_callback_matching(
        self, handler, sample_payment_notification
    ):
        """Test pattern-based callback matching."""
        callback_called = False

        @handler.register_callback("payment.*")
        def callback(payment: Payment):
            nonlocal callback_called
            callback_called = True

        notification = handler.parse_notification(sample_payment_notification)
        await handler.handle_notification(notification)

        assert callback_called is True

    @pytest.mark.asyncio
    async def test_multiple_callbacks_priority(
        self, handler, sample_payment_notification
    ):
        """Test that exact match callback takes priority over pattern."""
        exact_called = False
        pattern_called = False

        @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
        def exact_callback(payment: Payment):
            nonlocal exact_called
            exact_called = True

        @handler.register_callback("payment.*")
        def pattern_callback(payment: Payment):
            nonlocal pattern_called
            pattern_called = True

        notification = handler.parse_notification(sample_payment_notification)
        await handler.handle_notification(notification)

        # Exact match should be called, pattern should not
        assert exact_called is True
        assert pattern_called is False

    @pytest.mark.asyncio
    async def test_callback_error_handling(self, handler, sample_payment_notification):
        """Test error handling in callback."""

        @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
        async def failing_callback(payment: Payment):
            raise ValueError("Callback error")

        notification = handler.parse_notification(sample_payment_notification)

        with pytest.raises(ValueError, match="Callback error"):
            await handler.handle_notification(notification)

    @pytest.fixture
    def sample_payout_notification(self):
        """Sample payout notification data."""
        return {
            "type": "notification",
            "event": "payout.succeeded",
            "object": {
                "id": "payout_123",
                "status": "succeeded",
                "amount": {"value": "1000.00", "currency": "RUB"},
                "payout_destination": {
                    "type": "yoo_money",
                    "account_number": "4100111111111111",
                },
                "created_at": "2023-01-01T00:00:00.000Z",
                "test": False,
            },
        }

    @pytest.fixture
    def sample_deal_notification(self):
        """Sample deal notification data."""
        return {
            "type": "notification",
            "event": "deal.closed",
            "object": {
                "id": "deal_123",
                "type": "safe_deal",
                "status": "closed",
                "fee_moment": "payment_succeeded",
                "balance": {"value": "1000.00", "currency": "RUB"},
                "payout_balance": {"value": "900.00", "currency": "RUB"},
                "created_at": "2023-01-01T00:00:00.000Z",
                "expires_at": "2023-12-31T23:59:59.000Z",
                "test": False,
            },
        }

    @pytest.fixture
    def sample_payment_method_notification(self):
        """Sample payment method notification data."""
        return {
            "type": "notification",
            "event": "payment_method.active",
            "object": {
                "id": "pm_123",
                "type": "bank_card",
                "saved": True,
                "status": "active",
            },
        }

    @pytest.mark.asyncio
    async def test_handle_notification_payout(
        self, handler, sample_payout_notification
    ):
        """Test handling payout notification."""
        notification = handler.parse_notification(sample_payout_notification)
        event_object = await handler.handle_notification(notification)

        from aioyookassa.types.payout import Payout

        assert isinstance(event_object, Payout)
        assert event_object.id == "payout_123"

    @pytest.mark.asyncio
    async def test_handle_notification_deal(self, handler, sample_deal_notification):
        """Test handling deal notification."""
        notification = handler.parse_notification(sample_deal_notification)
        event_object = await handler.handle_notification(notification)

        from aioyookassa.types.deals import Deal

        assert isinstance(event_object, Deal)
        assert event_object.id == "deal_123"

    @pytest.mark.asyncio
    async def test_handle_notification_payment_method(
        self, handler, sample_payment_method_notification
    ):
        """Test handling payment method notification."""
        notification = handler.parse_notification(sample_payment_method_notification)
        event_object = await handler.handle_notification(notification)

        from aioyookassa.types.payment import PaymentMethod

        assert isinstance(event_object, PaymentMethod)
        assert event_object.id == "pm_123"

    @pytest.mark.asyncio
    async def test_handle_unknown_event_type(self, handler):
        """Test handling unknown event type."""
        notification_data = {
            "type": "notification",
            "event": "unknown.event",
            "object": {"id": "test_123", "data": "test"},
        }
        notification = handler.parse_notification(notification_data)
        event_object = await handler.handle_notification(notification)

        # Should return raw dict for unknown events
        assert isinstance(event_object, dict)
        assert event_object["id"] == "test_123"

    @pytest.mark.asyncio
    async def test_handle_parsing_error_returns_raw_dict(self, handler):
        """Test that parsing errors return raw dict instead of raising."""
        notification_data = {
            "type": "notification",
            "event": "payment.succeeded",
            "object": {
                # Invalid payment data (missing required fields)
                "id": "payment_123",
                # Missing required fields like status, amount, recipient, etc.
            },
        }
        notification = handler.parse_notification(notification_data)
        event_object = await handler.handle_notification(notification)

        # Should return raw dict when parsing fails
        assert isinstance(event_object, dict)
        assert event_object["id"] == "payment_123"
