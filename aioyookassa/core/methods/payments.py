from typing import Optional, List

from aioyookassa.types.payment import PaymentAmount, Receipt, Airline, Transfer, Deal
from .base import APIMethod, PaymentMethod


class CreatePayment(APIMethod):
    """
    Create payment
    """
    http_method = "POST"
    path = "/payments"

    @staticmethod
    def build_params(**kwargs):
        if confirmation := kwargs.get("confirmation"):
            kwargs["confirmation"] = confirmation.dict(exclude_none=True)
        params = {
            "amount": kwargs.get("amount").dict(),
            "description": kwargs.get("description"),
            "receipt": kwargs.get("receipt"),
            "recipient": kwargs.get("recipient"),
            "payment_token": kwargs.get("payment_token"),
            "payment_method_id": kwargs.get("payment_method_id"),
            "payment_method_data": kwargs.get("payment_method_data"),
            "confirmation": kwargs.get("confirmation"),
            "save_payment_method": kwargs.get("save_payment_method"),
            "capture": kwargs.get("capture"),
            "client_ip": kwargs.get("client_ip"),
            "metadata": kwargs.get("metadata"),
            "airline": kwargs.get("airline"),
            "transfers": kwargs.get("transfers"),
            "deal": kwargs.get("deal"),
            "merchant_customer_id": kwargs.get("merchant_customer_id"),
        }
        return params


class GetPayments(APIMethod):
    """
    Get Payments
    """
    http_method = "GET"
    path = "/payments"

    @staticmethod
    def build_params(created_at, captured_at,
                     payment_method, status,
                     limit, cursor, **kwargs):
        params = {
            "created_at_gte": created_at,
            "captured_at_gte": captured_at,
            "payment_method": payment_method.value if payment_method else None,
            "status": status.value if status else None,
            "limit": limit,
            "cursor": cursor,
            **kwargs
        }
        return params


class GetPayment(PaymentMethod):
    """
    Get Payment
    """
    http_method = "GET"
    path = "/payments/{payment_id}"


class CapturePayment(PaymentMethod):
    """
    Capture Payment
    """
    http_method = "POST"
    path = "/payments/{payment_id}/capture"

    @staticmethod
    def build_params(amount: Optional[PaymentAmount],
                     receipt: Optional[Receipt],
                     airline: Optional[Airline],
                     transfers: Optional[List[Transfer]],
                     deal: Optional[Deal]):
        params = {
            "amount": amount.dict() if amount else None,
            "receipt": receipt.dict() if receipt else None,
            "airline": airline.dict() if airline else None,
            "transfers": [transfer.dict() for transfer in transfers] if transfers else None,
            "deal": deal.dict() if deal else None,
        }
        return params


class CancelPayment(PaymentMethod):
    http_method = "POST"
    path = "/payments/{payment_id}/cancel"
