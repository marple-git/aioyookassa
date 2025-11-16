from typing import Any, Dict, List, Optional

from aioyookassa.core.utils import format_datetime_params, remove_none_values
from aioyookassa.types.payment import PaymentAmount, Receipt
from aioyookassa.types.refund import RefundDeal, RefundMethod, RefundSource

from .base import APIMethod, BaseAPIMethod


class RefundsAPIMethod(BaseAPIMethod):
    """
    Base class for refunds API methods.
    """

    http_method = "GET"
    path = "/refunds"

    @classmethod
    def build(cls, refund_id: str) -> "RefundsAPIMethod":  # type: ignore[override]
        """
        Build method for refund-specific endpoints.

        :param refund_id: Refund ID
        :return: Method instance
        """
        result = super().build(refund_id=refund_id)
        return result  # type: ignore[return-value]


class CreateRefund(RefundsAPIMethod):
    """
    Create refund.
    """

    http_method = "POST"  # type: ignore[assignment]

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        amount = kwargs.get("amount")
        receipt = kwargs.get("receipt")
        sources = kwargs.get("sources", [])
        deal = kwargs.get("deal")
        refund_method_data = kwargs.get("refund_method_data")

        params = {
            "payment_id": kwargs.get("payment_id"),
            "amount": APIMethod._safe_model_dump(
                amount, exclude_none=True, mode="python"
            ),
            "description": kwargs.get("description"),
            "receipt": APIMethod._safe_model_dump(
                receipt, exclude_none=True, mode="python"
            ),
            "sources": (
                [
                    APIMethod._safe_model_dump(source, exclude_none=True, mode="python")
                    for source in sources
                ]
                if sources
                else None
            ),
            "deal": APIMethod._safe_model_dump(deal, exclude_none=True, mode="python"),
            "refund_method_data": APIMethod._safe_model_dump(
                refund_method_data, exclude_none=True, mode="python"
            ),
        }
        return remove_none_values(params)


class GetRefunds(RefundsAPIMethod):
    """
    Get refunds list.
    """

    http_method = "GET"

    @staticmethod
    def build_params(
        created_at_gte: Any = None,
        created_at_gt: Any = None,
        created_at_lte: Any = None,
        created_at_lt: Any = None,
        payment_id: Any = None,
        status: Any = None,
        limit: Any = None,
        cursor: Any = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        params = {
            "created_at_gte": created_at_gte,
            "created_at_gt": created_at_gt,
            "created_at_lte": created_at_lte,
            "created_at_lt": created_at_lt,
            "payment_id": payment_id,
            "status": status,
            "limit": limit,
            "cursor": cursor,
            **kwargs,
        }
        # Format datetime fields
        params = format_datetime_params(
            params,
            ["created_at_gte", "created_at_gt", "created_at_lte", "created_at_lt"],
        )
        # Map to API field names
        result = {
            "created_at.gte": params.get("created_at_gte"),
            "created_at.gt": params.get("created_at_gt"),
            "created_at.lte": params.get("created_at_lte"),
            "created_at.lt": params.get("created_at_lt"),
            "payment_id": params.get("payment_id"),
            "status": params.get("status"),
            "limit": params.get("limit"),
            "cursor": params.get("cursor"),
        }
        result.update({k: v for k, v in kwargs.items() if k not in result})
        return remove_none_values(result)


class GetRefund(RefundsAPIMethod):
    """
    Get refund.
    """

    http_method = "GET"
    path = "/refunds/{refund_id}"
