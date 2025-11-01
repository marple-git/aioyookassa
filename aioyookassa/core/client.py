from typing import Optional, Union

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api import (
    InvoicesAPI,
    PaymentMethodsAPI,
    PaymentsAPI,
    ReceiptsAPI,
    RefundsAPI,
)
from aioyookassa.core.methods.me import GetMe
from aioyookassa.types.settings import Settings


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

    async def get_me(self, on_behalf_of: Optional[str] = None) -> Settings:
        """
        Get shop or gateway settings information.

        :param on_behalf_of: Shop ID for Split payments. Only for those who use Split payments.
        :type on_behalf_of: Optional[str]
        :returns: Settings object with shop or gateway information.
        :rtype: Settings
        :seealso: https://yookassa.ru/developers/api#me
        """
        params = GetMe.build_params(on_behalf_of=on_behalf_of)
        result = await self._send_request(GetMe, params=params)
        return Settings(**result)
