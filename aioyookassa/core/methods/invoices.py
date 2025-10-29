import datetime
from typing import Any, Dict, List, Optional, Union

from aioyookassa.types.invoice import (
    InvoiceCartItem,
    InvoiceDeliveryMethodData,
    InvoicePaymentData,
)

from .base import APIMethod


class InvoicesAPIMethod(APIMethod):
    """
    Base class for invoices API methods.
    """

    http_method = "GET"
    path = "/invoices"

    def __init__(self, path: Optional[str] = None) -> None:
        if path:
            self.path = path

    @classmethod
    def build(cls, invoice_id: str) -> "InvoicesAPIMethod":
        """
        Build method for invoice-specific endpoints.

        :param invoice_id: Invoice ID
        :return: Method instance
        """
        path = cls.path.format(invoice_id=invoice_id)
        return cls(path=path)


class CreateInvoice(InvoicesAPIMethod):
    """
    Create invoice.
    """

    http_method = "POST"

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

        if payment_data:
            payment_data_dict = payment_data.model_dump(
                exclude_none=True, mode="python"
            )
        else:
            payment_data_dict = None

        params = {
            "payment_data": payment_data_dict,
            "cart": (
                [item.model_dump(exclude_none=True, mode="python") for item in cart]
                if cart
                else None
            ),
            "delivery_method_data": (
                delivery_method_data.model_dump(exclude_none=True, mode="python")
                if delivery_method_data
                else None
            ),
            "expires_at": expires_at,
            "locale": kwargs.get("locale"),
            "description": kwargs.get("description"),
            "metadata": kwargs.get("metadata"),
        }
        return {k: v for k, v in params.items() if v is not None}


class GetInvoice(InvoicesAPIMethod):
    """
    Get invoice.
    """

    http_method = "GET"
    path = "/invoices/{invoice_id}"
