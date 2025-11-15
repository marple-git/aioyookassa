"""
Webhook event handler for YooKassa notifications.
"""

import asyncio
import logging
import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pydantic import ValidationError

from aioyookassa.core.webhook_validator import WebhookIPValidator
from aioyookassa.exceptions.webhooks import InvalidWebhookDataError
from aioyookassa.types.deals import Deal
from aioyookassa.types.enum import WebhookEvent
from aioyookassa.types.payment import Payment, PaymentMethod
from aioyookassa.types.payout import Payout
from aioyookassa.types.refund import Refund
from aioyookassa.types.webhook_notification import WebhookNotification

logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Handler for processing YooKassa webhook notifications.

    Provides functionality to:
    - Parse webhook notifications
    - Validate IP addresses (optional)
    - Register callbacks for specific events
    - Automatically parse event objects into typed Pydantic models
    """

    def __init__(
        self,
        validator: Optional[WebhookIPValidator] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize webhook handler.

        :param validator: IP validator instance. If None, creates default validator
                         with YooKassa official IP ranges.
        :param logger: Logger instance. If None, uses default logger.
        """
        self.validator = validator if validator is not None else WebhookIPValidator()
        self.logger = logger if logger is not None else logging.getLogger(__name__)
        self.callbacks: Dict[str, Callable] = {}
        self.pattern_callbacks: List[Tuple[re.Pattern, Callable]] = []

    def register_callback(
        self,
        events: Union[WebhookEvent, str, List[Union[WebhookEvent, str]]],
        callback: Optional[Callable] = None,
    ) -> Callable:
        """
        Decorator for registering event callbacks.

        Supports:
        - Single event: @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
        - Multiple events: @handler.register_callback([event1, event2])
        - Pattern matching: @handler.register_callback("payment.*")

        :param events: Event(s) to register callback for.
        :param callback: Callback function (used when called as decorator).
        :return: Decorator function or callback.
        """

        def decorator(func: Callable) -> Callable:
            self._register_events(events, func)
            return func

        return decorator

    def add_callback(
        self,
        events: Union[WebhookEvent, str, List[Union[WebhookEvent, str]]],
        callback: Callable,
    ) -> None:
        """
        Register callback without using decorator syntax.

        :param events: Event(s) to register callback for.
        :param callback: Callback function to register.
        """
        self._register_events(events, callback)

    def _register_events(
        self,
        events: Union[WebhookEvent, str, List[Union[WebhookEvent, str]]],
        callback: Callable,
    ) -> None:
        """Internal method to register events for a callback."""
        if isinstance(events, (WebhookEvent, str)):
            events_list = [events]
        else:
            events_list = events

        for event in events_list:
            event_str = str(event) if isinstance(event, WebhookEvent) else event

            if self._is_pattern(event_str):
                pattern = self._compile_pattern(event_str)
                self.pattern_callbacks.append((pattern, callback))
                self.logger.debug(
                    f"Registered pattern callback: pattern={event_str}, "
                    f"callback={callback.__name__}"
                )
            else:
                self.callbacks[event_str] = callback
                self.logger.debug(
                    f"Registered callback: event={event_str}, "
                    f"callback={callback.__name__}"
                )

    def _is_pattern(self, event: str) -> bool:
        """Check if event string is a pattern (contains wildcards)."""
        return "*" in event or "?" in event

    def _compile_pattern(self, pattern: str) -> re.Pattern:
        """Compile wildcard pattern into regex."""
        regex = (
            "^" + pattern.replace(".", r"\.").replace("*", ".*").replace("?", ".") + "$"
        )
        return re.compile(regex)

    def parse_notification(self, data: dict) -> WebhookNotification:
        """
        Parse raw webhook data into WebhookNotification model.

        :param data: Raw JSON data from webhook request.
        :return: Parsed WebhookNotification instance.
        :raises InvalidWebhookDataError: If data is invalid.
        """
        try:
            notification = WebhookNotification(**data)
            self.logger.debug(
                f"Parsed webhook notification: event={notification.event}, "
                f"type={notification.type}"
            )
            return notification
        except ValidationError as e:
            self.logger.error(f"Failed to parse webhook notification: {e}")
            raise InvalidWebhookDataError(
                f"Invalid webhook notification data: {e}"
            ) from e

    async def handle_notification(
        self, notification: WebhookNotification
    ) -> Union[Payment, Refund, Payout, Deal, PaymentMethod, dict]:
        """
        Process webhook notification and return typed event object.

        Automatically parses the notification object into the appropriate
        Pydantic model based on event type and calls registered callbacks.

        :param notification: Parsed webhook notification.
        :return: Typed event object (Payment, Refund, Payout, Deal, PaymentMethod).
        """
        event = notification.event
        self.logger.info(f"Processing webhook notification: event={event}")

        event_object = self._parse_object(notification)
        object_type = type(event_object).__name__
        self.logger.debug(
            f"Parsed event object: type={object_type}, "
            f"id={getattr(event_object, 'id', 'N/A')}"
        )

        # Find and call appropriate callback
        callback = self._find_callback(event)
        if callback:
            self.logger.debug(f"Found callback for event: {event}")
            try:
                await self._call_callback(callback, event_object)
                self.logger.debug(f"Successfully called callback for event: {event}")
            except Exception as e:
                self.logger.error(
                    f"Error in callback for event {event}: {e}", exc_info=True
                )
                raise
        else:
            self.logger.debug(f"No callback registered for event: {event}")

        self.logger.info(f"Successfully processed webhook notification: event={event}")
        return event_object

    def _parse_object(
        self, notification: WebhookNotification
    ) -> Union[Payment, Refund, Payout, Deal, PaymentMethod, dict]:
        """Parse notification object into appropriate Pydantic type."""
        event = notification.event
        obj_data = notification.object

        try:
            parsed: Union[Payment, Refund, Payout, Deal, PaymentMethod, dict]
            if event.startswith("payment."):
                parsed = Payment(**obj_data)
                self.logger.debug(f"Parsed Payment object: id={parsed.id}")
                return parsed
            elif event.startswith("refund."):
                parsed = Refund(**obj_data)
                self.logger.debug(f"Parsed Refund object: id={parsed.id}")
                return parsed
            elif event.startswith("payout."):
                parsed = Payout(**obj_data)
                self.logger.debug(f"Parsed Payout object: id={parsed.id}")
                return parsed
            elif event == WebhookEvent.DEAL_CLOSED:
                parsed = Deal(**obj_data)
                self.logger.debug(f"Parsed Deal object: id={parsed.id}")
                return parsed
            elif event == WebhookEvent.PAYMENT_METHOD_ACTIVE:
                parsed = PaymentMethod(**obj_data)
                self.logger.debug(f"Parsed PaymentMethod object: id={parsed.id}")
                return parsed
            else:
                # Unknown event type, return raw dict
                self.logger.warning(f"Unknown event type: {event}, returning raw dict")
                return obj_data
        except (ValidationError, TypeError) as e:
            # If parsing fails, return raw dict
            # This allows handling of events with unknown structure
            self.logger.warning(
                f"Failed to parse event object for {event}: {e}, " "returning raw dict"
            )
            return obj_data

    def _find_callback(self, event: str) -> Optional[Callable]:
        """Find callback for given event (exact match or pattern)."""
        # Check exact matches first
        if event in self.callbacks:
            return self.callbacks[event]

        # Check patterns
        for pattern, callback in self.pattern_callbacks:
            if pattern.match(event):
                return callback

        return None

    async def _call_callback(self, callback: Callable, event_object: Any) -> None:
        """Call callback function (sync or async)."""
        if asyncio.iscoroutinefunction(callback):
            await callback(event_object)
        else:
            callback(event_object)
