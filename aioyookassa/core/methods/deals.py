"""
Deals API methods.
"""

from typing import Any, Dict

from aioyookassa.core.utils import format_datetime_params, remove_none_values

from .base import APIMethod, BaseAPIMethod


class DealsAPIMethod(BaseAPIMethod):
    """
    Base class for deals API methods.
    """

    http_method = "GET"
    path = "/deals"

    @classmethod
    def build(cls, deal_id: str) -> "DealsAPIMethod":  # type: ignore[override]
        """
        Build method for deal-specific endpoints.

        :param deal_id: Deal ID
        :return: Method instance
        """
        result = super().build(deal_id=deal_id)
        return result  # type: ignore[return-value]


class CreateDeal(DealsAPIMethod):
    """
    Create deal.
    """

    http_method = "POST"  # type: ignore[assignment]

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        params = {
            "type": kwargs.get("type", "safe_deal"),
            "fee_moment": kwargs.get("fee_moment"),
            "metadata": kwargs.get("metadata"),
            "description": kwargs.get("description"),
        }
        return remove_none_values(params)


class GetDeals(DealsAPIMethod):
    """
    Get deals list.
    """

    http_method = "GET"

    @staticmethod
    def build_params(
        created_at_gte: Any = None,
        created_at_gt: Any = None,
        created_at_lte: Any = None,
        created_at_lt: Any = None,
        expires_at_gte: Any = None,
        expires_at_gt: Any = None,
        expires_at_lte: Any = None,
        expires_at_lt: Any = None,
        status: Any = None,
        full_text_search: Any = None,
        limit: Any = None,
        cursor: Any = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        params = {
            "created_at_gte": created_at_gte,
            "created_at_gt": created_at_gt,
            "created_at_lte": created_at_lte,
            "created_at_lt": created_at_lt,
            "expires_at_gte": expires_at_gte,
            "expires_at_gt": expires_at_gt,
            "expires_at_lte": expires_at_lte,
            "expires_at_lt": expires_at_lt,
            "status": status,
            "full_text_search": full_text_search,
            "limit": limit,
            "cursor": cursor,
            **kwargs,
        }
        # Format datetime fields
        params = format_datetime_params(
            params,
            [
                "created_at_gte",
                "created_at_gt",
                "created_at_lte",
                "created_at_lt",
                "expires_at_gte",
                "expires_at_gt",
                "expires_at_lte",
                "expires_at_lt",
            ],
        )
        # Map to API field names with dots
        result = {
            "created_at.gte": params.get("created_at_gte"),
            "created_at.gt": params.get("created_at_gt"),
            "created_at.lte": params.get("created_at_lte"),
            "created_at.lt": params.get("created_at_lt"),
            "expires_at.gte": params.get("expires_at_gte"),
            "expires_at.gt": params.get("expires_at_gt"),
            "expires_at.lte": params.get("expires_at_lte"),
            "expires_at.lt": params.get("expires_at_lt"),
            "status": params.get("status"),
            "full_text_search": params.get("full_text_search"),
            "limit": params.get("limit"),
            "cursor": params.get("cursor"),
        }
        result.update({k: v for k, v in kwargs.items() if k not in result})
        return remove_none_values(result)


class GetDeal(DealsAPIMethod):
    """
    Get deal.
    """

    http_method = "GET"
    path = "/deals/{deal_id}"
