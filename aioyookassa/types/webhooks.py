"""
Webhook types for YooKassa API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class Webhook(BaseModel):
    """
    Webhook object

    Contains information about a subscription to a single event.
    """

    id: str
    event: str
    url: str


class WebhooksList(BaseModel):
    """
    List of webhooks
    """

    list: Optional[List[Webhook]] = Field(None, alias="items")
