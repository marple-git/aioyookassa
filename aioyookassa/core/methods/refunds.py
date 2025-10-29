import datetime
from typing import Any, Dict, List, Optional

from aioyookassa.types.payment import PaymentAmount, Receipt
from aioyookassa.types.refund import RefundDeal, RefundMethod, RefundSource

from .base import APIMethod


class RefundsAPIMethod(APIMethod):
    """
    Base class for refunds API methods.
    """

    http_method = "GET"
    path = "/refunds"

    def __init__(self, path: Optional[str] = None) -> None:
        if path:
            self.path = path

    @classmethod
    def build(cls, refund_id: str) -> "RefundsAPIMethod":
        """
        Build method for refund-specific endpoints.

        :param refund_id: Refund ID
        :return: Method instance
        """
        path = cls.path.format(refund_id=refund_id)
        return cls(path=path)


class CreateRefund(RefundsAPIMethod):
    """
    Create refund.
    """

    http_method = "POST"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        amount = kwargs.get("amount")
        receipt = kwargs.get("receipt")
        sources = kwargs.get("sources", [])
        deal = kwargs.get("deal")
        refund_method_data = kwargs.get("refund_method_data")

        params = {
            "payment_id": kwargs.get("payment_id"),
            "amount": (
                amount.model_dump(exclude_none=True, mode="python") if amount else None
            ),
            "description": kwargs.get("description"),
            "receipt": (
                receipt.model_dump(exclude_none=True, mode="python")
                if receipt
                else None
            ),
            "sources": (
                [
                    source.model_dump(exclude_none=True, mode="python")
                    for source in sources
                ]
                if sources
                else None
            ),
            "deal": deal.model_dump(exclude_none=True, mode="python") if deal else None,
            "refund_method_data": (
                refund_method_data.model_dump(exclude_none=True, mode="python")
                if refund_method_data
                else None
            ),
        }
        return {k: v for k, v in params.items() if v is not None}


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
        # Format datetime if it's a datetime object
        if created_at_gte and isinstance(created_at_gte, datetime.datetime):
            created_at_gte = created_at_gte.isoformat()
        if created_at_gt and isinstance(created_at_gt, datetime.datetime):
            created_at_gt = created_at_gt.isoformat()
        if created_at_lte and isinstance(created_at_lte, datetime.datetime):
            created_at_lte = created_at_lte.isoformat()
        if created_at_lt and isinstance(created_at_lt, datetime.datetime):
            created_at_lt = created_at_lt.isoformat()

        params = {
            "created_at.gte": created_at_gte,
            "created_at.gt": created_at_gt,
            "created_at.lte": created_at_lte,
            "created_at.lt": created_at_lt,
            "payment_id": payment_id,
            "status": status,
            "limit": limit,
            "cursor": cursor,
            **kwargs,
        }
        return {k: v for k, v in params.items() if v is not None}


class GetRefund(RefundsAPIMethod):
    """
    Get refund.
    """

    http_method = "GET"
    path = "/refunds/{refund_id}"
