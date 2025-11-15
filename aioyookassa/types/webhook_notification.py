"""
Webhook notification types for YooKassa API.
"""

from typing import Literal

from pydantic import BaseModel


class WebhookNotification(BaseModel):
    """
    Webhook notification from YooKassa.

    Contains information about an event that occurred in YooKassa.
    The object field contains the actual event data (Payment, Refund, Payout, etc.)
    which should be parsed based on the event type.
    """

    type: Literal["notification"]
    event: str
    object: dict
