import datetime
from typing import Any, Dict, List, Optional

from aioyookassa.types.payment import Customer, IndustryDetails, OperationDetails
from aioyookassa.types.receipt_registration import (
    AdditionalUserProps,
    ReceiptRegistrationItem,
    ReceiptSettlement,
)

from .base import APIMethod


class ReceiptsAPIMethod(APIMethod):
    """
    Base class for receipts API methods.
    """

    http_method = "GET"
    path = "/receipts"

    def __init__(self, path: Optional[str] = None) -> None:
        if path:
            self.path = path

    @classmethod
    def build(cls, receipt_id: str) -> "ReceiptsAPIMethod":
        """
        Build method for receipt-specific endpoints.

        :param receipt_id: Receipt ID
        :return: Method instance
        """
        path = cls.path.format(receipt_id=receipt_id)
        return cls(path=path)


class CreateReceipt(ReceiptsAPIMethod):
    """
    Create receipt.
    """

    http_method = "POST"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        customer = kwargs.get("customer")
        items = kwargs.get("items", [])
        additional_user_props = kwargs.get("additional_user_props")
        receipt_industry_details = kwargs.get("receipt_industry_details", [])
        receipt_operational_details = kwargs.get("receipt_operational_details")

        params = {
            "type": kwargs.get("type"),
            "payment_id": kwargs.get("payment_id"),
            "refund_id": kwargs.get("refund_id"),
            "customer": (
                customer.model_dump(exclude_none=True, mode="python")
                if customer
                else None
            ),
            "items": (
                [item.model_dump(exclude_none=True, mode="python") for item in items]
                if items
                else None
            ),
            "send": kwargs.get("send", True),  # Always true according to documentation
            "internet": kwargs.get("internet"),
            "tax_system_code": kwargs.get("tax_system_code"),
            "timezone": kwargs.get("timezone"),
            "additional_user_props": (
                additional_user_props.model_dump(exclude_none=True, mode="python")
                if additional_user_props
                else None
            ),
            "receipt_industry_details": (
                [
                    detail.model_dump(exclude_none=True, mode="python")
                    for detail in receipt_industry_details
                ]
                if receipt_industry_details
                else None
            ),
            "receipt_operational_details": (
                receipt_operational_details.model_dump(exclude_none=True, mode="python")
                if receipt_operational_details
                else None
            ),
            "settlements": (
                [
                    settlement.model_dump(exclude_none=True, mode="python")
                    for settlement in kwargs.get("settlements", [])
                ]
                if kwargs.get("settlements")
                else None
            ),
            "on_behalf_of": kwargs.get("on_behalf_of"),
        }
        return {k: v for k, v in params.items() if v is not None}


class GetReceipts(ReceiptsAPIMethod):
    """
    Get receipts list.
    """

    http_method = "GET"

    @staticmethod
    def build_params(
        created_at_gte: Any = None,
        created_at_gt: Any = None,
        created_at_lte: Any = None,
        created_at_lt: Any = None,
        payment_id: Any = None,
        refund_id: Any = None,
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
            "refund_id": refund_id,
            "status": status,
            "limit": limit,
            "cursor": cursor,
            **kwargs,
        }
        return {k: v for k, v in params.items() if v is not None}


class GetReceipt(ReceiptsAPIMethod):
    """
    Get receipt.
    """

    http_method = "GET"
    path = "/receipts/{receipt_id}"
