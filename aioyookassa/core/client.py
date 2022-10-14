import uuid
from typing import Union, Optional, Any, List

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods import CreatePayment
from aioyookassa.types import Confirmation, Payment


class YooKassa(BaseAPIClient):
    """YooKassa API Client"""

    def __init__(self, api_key: str, shop_id: int):
        super().__init__(api_key, shop_id)

    async def create_payment(self, currency: str, amount: Union[int, float],
                             description: Optional[str] = None,
                             receipt: Optional[dict] = None,
                             recipient: Optional[dict] = None,
                             payment_token: Optional[str] = None,
                             payment_method_id: Optional[str] = None,
                             payment_method_data: Optional[dict] = None,
                             confirmation: Optional[Confirmation] = None,
                             save_payment_method: Optional[bool] = False,
                             capture: Optional[bool] = False,
                             client_ip: Optional[str] = None,
                             metadata: Optional[Any] = None,
                             airline: Optional[dict] = None,
                             transfers: Optional[List[dict]] = None,
                             deal: Optional[dict] = None,
                             merchant_customer_id: Optional[str] = None
                             ) -> Payment:
        """
        Create payment
        More detailed documentation:
        https://yookassa.ru/developers/api?codeLang=bash#create_payment

        :param merchant_customer_id: Payer ID in the merchant's system
        :param deal: Deal data
        :param transfers: Money distribution data
        :param airline: Object with data for selling air tickets
        :param metadata: Any additional data
        :param client_ip: IPv4 or IPv6 address of the payer
        :param capture: Automatic acceptance of incoming payment
        :param save_payment_method: Save payment data
        :param confirmation:
        :param payment_method_data: Payment method
        :param payment_method_id: Saved payment method ID
        :param payment_token: One-time payment token
        :param recipient: Payment receiver
        :param receipt: Recept generation data
        :param amount: Payment Amount
        :param currency: Payment Currency
        :param description: Payment Description
        :return: JSON
        """

        params = CreatePayment.build_params(**locals())
        headers = {'Idempotence-Key': str(uuid.uuid4())}
        result = await self._send_request(CreatePayment, params, headers)
        return Payment(**result)
