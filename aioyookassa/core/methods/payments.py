from typing import Optional, List

from aioyookassa.types.payment import PaymentAmount, Receipt, Airline, Transfer, Deal
from .base import APIMethod


class PaymentsAPIMethod(APIMethod):
    """
    Base class for payments API methods.
    """
    http_method = "GET"
    path = "/payments"

    def __init__(self, path: str = None):
        if path:
            self.path = path

    @classmethod
    def build(cls, payment_id):
        """
        Build method for payment-specific endpoints
        :param payment_id: Payment ID
        :return: Method instance
        """
        path = cls.path.format(payment_id=payment_id)
        return cls(path=path)


class CreatePayment(PaymentsAPIMethod):
    """
    Create payment
    """
    http_method = "POST"

    @staticmethod
    def build_params(**kwargs):
        if confirmation := kwargs.get("confirmation"):
            kwargs["confirmation"] = confirmation.model_dump(exclude_none=True)
        params = {
            "amount": kwargs.get("amount").model_dump() if kwargs.get("amount") else None,
            "description": kwargs.get("description"),
            "receipt": kwargs.get("receipt").model_dump() if kwargs.get("receipt") else None,
            "recipient": kwargs.get("recipient").model_dump() if kwargs.get("recipient") else None,
            "payment_token": kwargs.get("payment_token"),
            "payment_method_id": kwargs.get("payment_method_id"),
            "payment_method_data": kwargs.get("payment_method_data").model_dump() if kwargs.get("payment_method_data") else None,
            "confirmation": kwargs.get("confirmation"),
            "save_payment_method": kwargs.get("save_payment_method"),
            "capture": kwargs.get("capture"),
            "client_ip": kwargs.get("client_ip"),
            "metadata": kwargs.get("metadata"),
            "airline": kwargs.get("airline").model_dump() if kwargs.get("airline") else None,
            "transfers": [t.model_dump() for t in kwargs.get("transfers", [])] if kwargs.get("transfers") else None,
            "deal": kwargs.get("deal").model_dump() if kwargs.get("deal") else None,
            "merchant_customer_id": kwargs.get("merchant_customer_id"),
        }
        return params


class GetPayments(PaymentsAPIMethod):
    """
    Get Payments
    """
    http_method = "GET"

    @staticmethod
    def build_params(created_at, captured_at,
                     payment_method, status,
                     limit, cursor, **kwargs):
        params = {
            "created_at_gte": created_at,
            "captured_at_gte": captured_at,
            "payment_method": payment_method if payment_method else None,
            "status": status if status else None,
            "limit": limit,
            "cursor": cursor,
            **kwargs
        }
        return params


class GetPayment(PaymentsAPIMethod):
    """
    Get Payment
    """
    http_method = "GET"
    path = "/payments/{payment_id}"


class CapturePayment(PaymentsAPIMethod):
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
            "amount": amount.model_dump() if amount else None,
            "receipt": receipt.model_dump() if receipt else None,
            "airline": airline.model_dump() if airline else None,
            "transfers": [transfer.model_dump() for transfer in transfers] if transfers else None,
            "deal": deal.model_dump() if deal else None,
        }
        return params


class CancelPayment(PaymentsAPIMethod):
    """
    Cancel Payment
    """
    http_method = "POST"
    path = "/payments/{payment_id}/cancel"
