from typing import Union

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api import (
    InvoicesAPI,
    PaymentMethodsAPI,
    PaymentsAPI,
    ReceiptsAPI,
    RefundsAPI,
)


class YooKassa(BaseAPIClient):
    """
    YooKassa API Client.

    Main client for interacting with YooKassa payment system.
    Provides access to all available API modules:
    - payments: Payment operations
    - payment_methods: Payment method management
    - invoices: Invoice operations
    - refunds: Refund operations
    - receipts: Fiscal receipt operations
    """

    def __init__(self, api_key: str, shop_id: Union[int, str]):
        """
        Initialize YooKassa client.

        :param api_key: YooKassa API key
        :param shop_id: YooKassa shop ID
        """
        super().__init__(api_key, shop_id)
        self.payments = PaymentsAPI(self)
        self.payment_methods = PaymentMethodsAPI(self)
        self.invoices = InvoicesAPI(self)
        self.refunds = RefundsAPI(self)
        self.receipts = ReceiptsAPI(self)
