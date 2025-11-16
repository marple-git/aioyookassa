"""
Webhooks API methods.
"""

from typing import Any, Dict

from aioyookassa.core.utils import remove_none_values

from .base import BaseAPIMethod


class WebhooksAPIMethod(BaseAPIMethod):
    """
    Base class for webhooks API methods.
    """

    http_method = "GET"
    path = "/webhooks"

    @classmethod
    def build(cls, webhook_id: str) -> "WebhooksAPIMethod":  # type: ignore[override]
        """
        Build method for webhook-specific endpoints.

        :param webhook_id: Webhook ID
        :return: Method instance
        """
        result = super().build(webhook_id=webhook_id)
        return result  # type: ignore[return-value]


class CreateWebhook(WebhooksAPIMethod):
    """
    Create webhook.
    """

    http_method = "POST"  # type: ignore[assignment]

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        params = {
            "event": kwargs.get("event"),
            "url": kwargs.get("url"),
        }
        return remove_none_values(params)


class GetWebhooks(WebhooksAPIMethod):
    """
    Get webhooks list.
    """

    http_method = "GET"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        # No parameters for this endpoint
        return {}


class DeleteWebhook(WebhooksAPIMethod):
    """
    Delete webhook.
    """

    http_method = "DELETE"  # type: ignore[assignment]
    path = "/webhooks/{webhook_id}"
