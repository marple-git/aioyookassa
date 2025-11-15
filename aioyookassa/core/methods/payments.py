from typing import Any, Dict, List, Optional

from aioyookassa.core.utils import remove_none_values
from aioyookassa.types.payment import Airline, Deal, PaymentAmount, Receipt, Transfer

from .base import APIMethod, BaseAPIMethod


class PaymentsAPIMethod(BaseAPIMethod):
    """
    Base class for payments API methods.
    """

    http_method = "GET"
    path = "/payments"

    @classmethod
    def build(cls, payment_id: str) -> "PaymentsAPIMethod":  # type: ignore[override]
        """
        Build method for payment-specific endpoints.

        :param payment_id: Payment ID
        :return: Method instance
        """
        result = super().build(payment_id=payment_id)
        return result  # type: ignore[return-value]


class CreatePayment(PaymentsAPIMethod):
    """
    Create payment.
    """

    http_method = "POST"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        confirmation = kwargs.get("confirmation")
        if confirmation:
            kwargs["confirmation"] = APIMethod._safe_model_dump(
                confirmation, exclude_none=True
            )
        amount = kwargs.get("amount")
        receipt = kwargs.get("receipt")
        recipient = kwargs.get("recipient")
        payment_method_data = kwargs.get("payment_method_data")
        airline = kwargs.get("airline")
        transfers = kwargs.get("transfers")
        deal = kwargs.get("deal")

        params = {
            "amount": APIMethod._safe_model_dump(amount),
            "description": kwargs.get("description"),
            "receipt": APIMethod._safe_model_dump(receipt),
            "recipient": APIMethod._safe_model_dump(recipient),
            "payment_token": kwargs.get("payment_token"),
            "payment_method_id": kwargs.get("payment_method_id"),
            "payment_method_data": APIMethod._safe_model_dump(payment_method_data),
            "confirmation": kwargs.get("confirmation"),
            "save_payment_method": kwargs.get("save_payment_method"),
            "capture": kwargs.get("capture"),
            "client_ip": kwargs.get("client_ip"),
            "metadata": kwargs.get("metadata"),
            "airline": APIMethod._safe_model_dump(airline),
            "transfers": (
                [APIMethod._safe_model_dump(t) for t in transfers]
                if transfers
                else None
            ),
            "deal": APIMethod._safe_model_dump(deal),
            "merchant_customer_id": kwargs.get("merchant_customer_id"),
        }
        return remove_none_values(params)


class GetPayments(PaymentsAPIMethod):
    """
    Get payments.
    """

    http_method = "GET"

    @staticmethod
    def build_params(
        created_at: Any = None,
        captured_at: Any = None,
        payment_method: Any = None,
        status: Any = None,
        limit: Any = None,
        cursor: Any = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        params = {
            "created_at_gte": created_at,
            "captured_at_gte": captured_at,
            "payment_method": payment_method if payment_method else None,
            "status": status if status else None,
            "limit": limit,
            "cursor": cursor,
            **kwargs,
        }
        return remove_none_values(params)


class GetPayment(PaymentsAPIMethod):
    """
    Get payment.
    """

    http_method = "GET"
    path = "/payments/{payment_id}"


class CapturePayment(PaymentsAPIMethod):
    """
    Capture payment.
    """

    http_method = "POST"
    path = "/payments/{payment_id}/capture"

    @staticmethod
    def build_params(
        amount: Optional[PaymentAmount] = None,
        receipt: Optional[Receipt] = None,
        airline: Optional[Airline] = None,
        transfers: Optional[List[Transfer]] = None,
        deal: Optional[Deal] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        # Support both positional and keyword arguments
        amount = kwargs.get("amount", amount)
        receipt = kwargs.get("receipt", receipt)
        airline = kwargs.get("airline", airline)
        transfers = kwargs.get("transfers", transfers)
        deal = kwargs.get("deal", deal)

        params = {
            "amount": APIMethod._safe_model_dump(amount),
            "receipt": APIMethod._safe_model_dump(receipt),
            "airline": APIMethod._safe_model_dump(airline),
            "transfers": (
                [APIMethod._safe_model_dump(t) for t in transfers]
                if transfers
                else None
            ),
            "deal": APIMethod._safe_model_dump(deal),
        }
        return remove_none_values(params)


class CancelPayment(PaymentsAPIMethod):
    """
    Cancel payment.
    """

    http_method = "POST"
    path = "/payments/{payment_id}/cancel"
