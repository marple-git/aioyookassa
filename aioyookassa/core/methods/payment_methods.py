from typing import Dict, Any
from .base import APIMethod

class PaymentMethodBase(APIMethod):
    """
    Base class for payment method API methods.
    """
    path = "/payment_methods"

    def __init__(self, path: str = None):
        if path:
            self.path = path

class CreatePaymentMethod(PaymentMethodBase):
    """
    HTTP method for creating a payment method.
    API reference: https://yookassa.ru/developers/api#create_payment_method
    """
    http_method = "POST"

    @staticmethod
    def build_params(**kwargs) -> Dict[str, Any]:
        return kwargs

class GetPaymentMethod(PaymentMethodBase):
    """
    HTTP method for retrieving payment method information.
    API reference: https://yookassa.ru/developers/api#get_payment_method
    """
    http_method = "GET"

    @classmethod
    def build(cls, payment_method_id: str):
        """
        Build method for payment method specific endpoint
        :param payment_method_id: Payment method ID
        :return: Method instance
        """
        path = f"{cls.path}/{payment_method_id}"
        return cls(path=path)
