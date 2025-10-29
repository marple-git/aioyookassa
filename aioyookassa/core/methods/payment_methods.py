from typing import Any, Dict, Optional

from .base import APIMethod


class PaymentMethodBase(APIMethod):
    """
    Base class for payment method API methods.
    """

    http_method = "GET"
    path = "/payment_methods"

    def __init__(self, path: Optional[str] = None) -> None:
        if path:
            self.path = path

    @classmethod
    def build(cls, payment_method_id: str) -> "PaymentMethodBase":
        """
        Build method for payment method-specific endpoints.

        :param payment_method_id: Payment method ID
        :return: Method instance
        """
        path = cls.path.format(payment_method_id=payment_method_id)
        return cls(path=path)


class CreatePaymentMethod(PaymentMethodBase):
    """
    Create payment method.

    API reference: https://yookassa.ru/developers/api#create_payment_method
    """

    http_method = "POST"

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
