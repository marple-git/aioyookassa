from typing import Any, Dict

from .base import BaseAPIMethod


class PaymentMethodBase(BaseAPIMethod):
    """
    Base class for payment method API methods.
    """

    http_method = "GET"
    path = "/payment_methods"

    @classmethod
    def build(cls, payment_method_id: str) -> "PaymentMethodBase":  # type: ignore[override]
        """
        Build method for payment method-specific endpoints.

        :param payment_method_id: Payment method ID
        :return: Method instance
        """
        result = super().build(payment_method_id=payment_method_id)
        return result  # type: ignore[return-value]


class CreatePaymentMethod(PaymentMethodBase):
    """
    Create payment method.

    API reference: https://yookassa.ru/developers/api#create_payment_method
    """

    http_method = "POST"  # type: ignore[assignment]

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        return kwargs


class GetPaymentMethod(PaymentMethodBase):
    """
    Get payment method information.

    API reference: https://yookassa.ru/developers/api#get_payment_method
    """

    http_method = "GET"
    path = "/payment_methods/{payment_method_id}"
