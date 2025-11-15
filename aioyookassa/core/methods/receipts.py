from typing import Any, Dict, List, Optional

from aioyookassa.core.utils import format_datetime_params, remove_none_values
from aioyookassa.types.payment import (
    Customer,
    IndustryDetails,
    OperationDetails,
    Settlement,
)
from aioyookassa.types.receipt_registration import (
    AdditionalUserProps,
    ReceiptRegistrationItem,
)

from .base import APIMethod, BaseAPIMethod


class ReceiptsAPIMethod(BaseAPIMethod):
    """
    Base class for receipts API methods.
    """

    http_method = "GET"
    path = "/receipts"

    @classmethod
    def build(cls, receipt_id: str) -> "ReceiptsAPIMethod":  # type: ignore[override]
        """
        Build method for receipt-specific endpoints.

        :param receipt_id: Receipt ID
        :return: Method instance
        """
        result = super().build(receipt_id=receipt_id)
        return result  # type: ignore[return-value]


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

        settlements = kwargs.get("settlements", [])

        params = {
            "type": kwargs.get("type"),
            "payment_id": kwargs.get("payment_id"),
            "refund_id": kwargs.get("refund_id"),
            "customer": APIMethod._safe_model_dump(
                customer, exclude_none=True, mode="python"
            ),
            "items": (
                [
                    APIMethod._safe_model_dump(item, exclude_none=True, mode="python")
                    for item in items
                ]
                if items
                else None
            ),
            "send": kwargs.get("send", True),  # Always true according to documentation
            "internet": kwargs.get("internet"),
            "tax_system_code": kwargs.get("tax_system_code"),
            "timezone": kwargs.get("timezone"),
            "additional_user_props": APIMethod._safe_model_dump(
                additional_user_props, exclude_none=True, mode="python"
            ),
            "receipt_industry_details": (
                [
                    APIMethod._safe_model_dump(detail, exclude_none=True, mode="python")
                    for detail in receipt_industry_details
                ]
                if receipt_industry_details
                else None
            ),
            "receipt_operational_details": APIMethod._safe_model_dump(
                receipt_operational_details, exclude_none=True, mode="python"
            ),
            "settlements": (
                [
                    APIMethod._safe_model_dump(
                        settlement, exclude_none=True, mode="python"
                    )
                    for settlement in settlements
                ]
                if settlements
                else None
            ),
            "on_behalf_of": kwargs.get("on_behalf_of"),
        }
        return remove_none_values(params)


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
        params = {
            "created_at_gte": created_at_gte,
            "created_at_gt": created_at_gt,
            "created_at_lte": created_at_lte,
            "created_at_lt": created_at_lt,
            "payment_id": payment_id,
            "refund_id": refund_id,
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
            "refund_id": params.get("refund_id"),
            "status": params.get("status"),
            "limit": params.get("limit"),
            "cursor": params.get("cursor"),
        }
        result.update({k: v for k, v in kwargs.items() if k not in result})
        return remove_none_values(result)


class GetReceipt(ReceiptsAPIMethod):
    """
    Get receipt.
    """

    http_method = "GET"
    path = "/receipts/{receipt_id}"
