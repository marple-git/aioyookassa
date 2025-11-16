import datetime
from typing import Any, Dict, List, Optional, Union

from aioyookassa.core.utils import remove_none_values
from aioyookassa.types.invoice import (
    InvoiceCartItem,
    InvoiceDeliveryMethodData,
    InvoicePaymentData,
)

from .base import APIMethod, BaseAPIMethod


class InvoicesAPIMethod(BaseAPIMethod):
    """
    Base class for invoices API methods.
    """

    http_method = "GET"
    path = "/invoices"

    @classmethod
    def build(cls, invoice_id: str) -> "InvoicesAPIMethod":  # type: ignore[override]
        """
        Build method for invoice-specific endpoints.

        :param invoice_id: Invoice ID
        :return: Method instance
        """
        result = super().build(invoice_id=invoice_id)
        return result  # type: ignore[return-value]


class CreateInvoice(InvoicesAPIMethod):
    """
    Create invoice.
    """

    http_method = "POST"  # type: ignore[assignment]

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        expires_at = kwargs.get("expires_at")
        if isinstance(expires_at, datetime.datetime):
            if expires_at.tzinfo is not None:
                expires_at = expires_at.astimezone(datetime.timezone.utc)
            expires_at = expires_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        payment_data = kwargs.get("payment_data")
        cart = kwargs.get("cart", [])
        delivery_method_data = kwargs.get("delivery_method_data")

        params = {
            "payment_data": APIMethod._safe_model_dump(
                payment_data, exclude_none=True, mode="python"
            ),
            "cart": (
                [
                    APIMethod._safe_model_dump(item, exclude_none=True, mode="python")
                    for item in cart
                ]
                if cart
                else None
            ),
            "delivery_method_data": APIMethod._safe_model_dump(
                delivery_method_data, exclude_none=True, mode="python"
            ),
            "expires_at": expires_at,
            "locale": kwargs.get("locale"),
            "description": kwargs.get("description"),
            "metadata": kwargs.get("metadata"),
        }
        return remove_none_values(params)


class GetInvoice(InvoicesAPIMethod):
    """
    Get invoice.
    """

    http_method = "GET"
    path = "/invoices/{invoice_id}"
