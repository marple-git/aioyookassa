from typing import Any, Dict, List, Optional

from aioyookassa.types.payment import Airline, Deal, PaymentAmount, Receipt, Transfer

from .base import APIMethod


class PaymentsAPIMethod(APIMethod):
    """
    Base class for payments API methods.
    """

    http_method = "GET"
    path = "/payments"

    def __init__(self, path: Optional[str] = None) -> None:
        if path:
            self.path = path

    @classmethod
    def build(cls, payment_id: str) -> "PaymentsAPIMethod":
        """
        Build method for payment-specific endpoints.

        :param payment_id: Payment ID
        :return: Method instance
        """
        path = cls.path.format(payment_id=payment_id)
        return cls(path=path)


class CreatePayment(PaymentsAPIMethod):
    """
    Create payment.
    """

    http_method = "POST"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        if confirmation := kwargs.get("confirmation"):
            kwargs["confirmation"] = confirmation.model_dump(exclude_none=True)
        amount = kwargs.get("amount")
        receipt = kwargs.get("receipt")
        recipient = kwargs.get("recipient")
        payment_method_data = kwargs.get("payment_method_data")
        airline = kwargs.get("airline")
        transfers = kwargs.get("transfers")
        deal = kwargs.get("deal")

        params = {
            "amount": amount.model_dump() if amount else None,
            "description": kwargs.get("description"),
            "receipt": receipt.model_dump() if receipt else None,
            "recipient": recipient.model_dump() if recipient else None,
            "payment_token": kwargs.get("payment_token"),
            "payment_method_id": kwargs.get("payment_method_id"),
            "payment_method_data": (
                payment_method_data.model_dump() if payment_method_data else None
            ),
            "confirmation": kwargs.get("confirmation"),
            "save_payment_method": kwargs.get("save_payment_method"),
            "capture": kwargs.get("capture"),
            "client_ip": kwargs.get("client_ip"),
            "metadata": kwargs.get("metadata"),
            "airline": airline.model_dump() if airline else None,
            "transfers": [t.model_dump() for t in transfers] if transfers else None,
            "deal": deal.model_dump() if deal else None,
            "merchant_customer_id": kwargs.get("merchant_customer_id"),
        }
        return {k: v for k, v in params.items() if v is not None}


class GetPayments(PaymentsAPIMethod):
    """
    Get payments.
    """

    http_method = "GET"

    @staticmethod
    def build_params(
        created_at: Any,
        captured_at: Any,
        payment_method: Any,
        status: Any,
        limit: Any,
        cursor: Any,
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
        return {k: v for k, v in params.items() if v is not None}


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
        amount: Optional[PaymentAmount],
        receipt: Optional[Receipt],
        airline: Optional[Airline],
        transfers: Optional[List[Transfer]],
        deal: Optional[Deal],
    ) -> Dict[str, Any]:
        params = {
            "amount": amount.model_dump() if amount else None,
            "receipt": receipt.model_dump() if receipt else None,
            "airline": airline.model_dump() if airline else None,
            "transfers": (
                [transfer.model_dump() for transfer in transfers] if transfers else None
            ),
            "deal": deal.model_dump() if deal else None,
        }
        return {k: v for k, v in params.items() if v is not None}


class CancelPayment(PaymentsAPIMethod):
    """
    Cancel payment.
    """

    http_method = "POST"
    path = "/payments/{payment_id}/cancel"
