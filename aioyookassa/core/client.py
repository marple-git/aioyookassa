import logging
from typing import Optional, Union

from aiohttp import ClientTimeout, TCPConnector

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.api import (
    DealsAPI,
    InvoicesAPI,
    PaymentMethodsAPI,
    PaymentsAPI,
    PayoutsAPI,
    PersonalDataAPI,
    ReceiptsAPI,
    RefundsAPI,
    SbpBanksAPI,
    SelfEmployedAPI,
    WebhooksAPI,
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
    - payouts: Payout operations
    - self_employed: Self-employed operations
    - sbp_banks: SBP participant banks operations
    - personal_data: Personal data operations
    - deals: Safe Deal operations
    - webhooks: Webhook operations (requires OAuth token)
    """

    def __init__(
        self,
        api_key: str,
        shop_id: Union[int, str],
        timeout: Optional[ClientTimeout] = None,
        connector: Optional[TCPConnector] = None,
        proxy: Optional[str] = None,
        enable_logging: bool = False,
        logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            api_key=api_key,
            shop_id=shop_id,
            timeout=timeout,
            connector=connector,
            proxy=proxy,
            enable_logging=enable_logging,
            logger=logger,
        )
        self.payments = PaymentsAPI(self)
        self.payment_methods = PaymentMethodsAPI(self)
        self.invoices = InvoicesAPI(self)
        self.refunds = RefundsAPI(self)
        self.receipts = ReceiptsAPI(self)
        self.payouts = PayoutsAPI(self)
        self.self_employed = SelfEmployedAPI(self)
        self.sbp_banks = SbpBanksAPI(self)
        self.personal_data = PersonalDataAPI(self)
        self.deals = DealsAPI(self)
        self.webhooks = WebhooksAPI(self)

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
