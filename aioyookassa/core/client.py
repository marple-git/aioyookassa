from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.payments import PaymentsAPI
from aioyookassa.core.payment_methods import PaymentMethodsAPI


class YooKassa(BaseAPIClient):
    """YooKassa API Client"""

    def __init__(self, api_key: str, shop_id: int):
        super().__init__(api_key, shop_id)
        self.payments = PaymentsAPI(self)
        self.payment_methods = PaymentMethodsAPI(self)
