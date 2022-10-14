import uuid
from datetime import datetime
from typing import Union, Optional, Any, List

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods import CreatePayment, GetPayments, GetPayment, CapturePayment, CancelPayment
from aioyookassa.types import Confirmation, Payment, PaymentsList
from aioyookassa.types.enum import PaymentMethodType, PaymentStatus
from aioyookassa.types.payment import PaymentAmount, Receipt, Airline, Transfer, Deal


class YooKassa(BaseAPIClient):
    """YooKassa API Client"""

    def __init__(self, api_key: str, shop_id: int):
        super().__init__(api_key, shop_id)

    async def create_payment(self, amount: PaymentAmount,
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
        :return: Payment
        """

        params = CreatePayment.build_params(**locals())
        headers = {'Idempotence-Key': self._get_idempotence_key()}
        result = await self._send_request(CreatePayment, json=params, headers=headers)
        return Payment(**result)

    async def get_payments(self, created_at: Optional[datetime] = None,
                           captured_at: Optional[datetime] = None,
                           payment_method: Optional[PaymentMethodType] = None,
                           status: Optional[PaymentStatus] = None,
                           limit: Optional[int] = None,
                           cursor: Optional[str] = None,
                           **kwargs) -> PaymentsList:
        """
        Get payments
        More detailed documentation:
        https://yookassa.ru/developers/api?codeLang=php#get_payments_list

        :param created_at: Created at [GTE]
        :param captured_at: Captured at [GTE]
        :param payment_method: Payment Method
        :param status: Payment Status
        :param limit: Objects limit
        :param cursor: Cursor
        :return: Payments List
        """
        params = GetPayments.build_params(created_at=created_at,
                                          captured_at=captured_at,
                                          payment_method=payment_method,
                                          status=status,
                                          limit=limit,
                                          cursor=cursor,
                                          **kwargs)
        result = await self._send_request(GetPayments, params=params)
        return PaymentsList(**result)

    async def get_payment(self, payment_id: str) -> Payment:
        """
        Get payment by id
        More detailed documentation:
        https://yookassa.ru/developers/api?codeLang=bash#get_payment

        :param payment_id: Payment ID
        :return: Payment Info
        """
        method = GetPayment.build(payment_id=payment_id)
        result = await self._send_request(method)
        return Payment(**result)

    async def capture_payment(self, payment_id: str,
                              amount: Optional[PaymentAmount] = None,
                              receipt: Optional[Receipt] = None,
                              airline: Optional[Airline] = None,
                              transfers: Optional[List[Transfer]] = None,
                              deal: Optional[Deal] = None) -> Payment:
        """
        Capture payment
        More detailed documentation:
        https://yookassa.ru/developers/api?codeLang=bash#capture_payment

        :param payment_id: Payment ID
        :param amount: Payment Amount
        :param receipt: Receipt Info
        :param airline: Airline
        :param transfers: Transfers
        :param deal: Deal
        :return: Payment
        """
        method = CapturePayment.build(payment_id=payment_id)
        params = method.build_params(
            amount=amount,
            receipt=receipt,
            airline=airline,
            transfers=transfers,
            deal=deal
        )
        headers = {'Idempotence-Key': self._get_idempotence_key()}
        result = await self._send_request(method, json=params, headers=headers)
        return Payment(**result)

    async def cancel_payment(self, payment_id: str) -> Payment:
        """
        Cancel payment
        More detailed documentation:
        https://yookassa.ru/developers/api#cancel_payment

        :param payment_id: Payment ID
        :return: Payment
        """
        method = CancelPayment.build(payment_id=payment_id)
        headers = {'Idempotence-Key': self._get_idempotence_key()}
        result = await self._send_request(method, headers=headers)
        return Payment(**result)

    @staticmethod
    def _get_idempotence_key() -> str:
        return str(uuid.uuid4())
