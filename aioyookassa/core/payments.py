from typing import Optional, Any, List
from datetime import datetime
import uuid

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods import CreatePayment, GetPayments, GetPayment, CapturePayment, CancelPayment
from aioyookassa.types import Confirmation, Payment, PaymentsList
from aioyookassa.types.enum import PaymentMethodType, PaymentStatus
from aioyookassa.types.payment import PaymentAmount, Receipt, Airline, Transfer, Deal, Recipient, PaymentMethod

class PaymentsAPI:
    def __init__(self, client: BaseAPIClient):
        self._client = client

    async def create_payment(self, amount: PaymentAmount,
                             description: Optional[str] = None,
                             receipt: Optional[Receipt] = None,
                             recipient: Optional[Recipient] = None,
                             payment_token: Optional[str] = None,
                             payment_method_id: Optional[str] = None,
                             payment_method_data: Optional[PaymentMethod] = None,
                             confirmation: Optional[Confirmation] = None,
                             save_payment_method: Optional[bool] = False,
                             capture: Optional[bool] = False,
                             client_ip: Optional[str] = None,
                             metadata: Optional[Any] = None,
                             airline: Optional[Airline] = None,
                             transfers: Optional[List[Transfer]] = None,
                             deal: Optional[Deal] = None,
                             merchant_customer_id: Optional[str] = None
                             ) -> Payment:
        params = CreatePayment.build_params(**locals())
        headers = {'Idempotence-Key': self._get_idempotence_key()}
        result = await self._client._send_request(CreatePayment, json=params, headers=headers)
        return Payment(**result)

    async def get_payments(self, created_at: Optional[datetime] = None,
                           captured_at: Optional[datetime] = None,
                           payment_method: Optional[PaymentMethodType] = None,
                           status: Optional[PaymentStatus] = None,
                           limit: Optional[int] = None,
                           cursor: Optional[str] = None,
                           **kwargs) -> PaymentsList:
        params = GetPayments.build_params(created_at=created_at,
                                          captured_at=captured_at,
                                          payment_method=payment_method,
                                          status=status,
                                          limit=limit,
                                          cursor=cursor,
                                          **kwargs)
        result = await self._client._send_request(GetPayments, params=params)
        return PaymentsList(**result)

    async def get_payment(self, payment_id: str) -> Payment:
        method = GetPayment.build(payment_id=payment_id)
        result = await self._client._send_request(method)
        return Payment(**result)

    async def capture_payment(self, payment_id: str,
                              amount: Optional[PaymentAmount] = None,
                              receipt: Optional[Receipt] = None,
                              airline: Optional[Airline] = None,
                              transfers: Optional[List[Transfer]] = None,
                              deal: Optional[Deal] = None) -> Payment:
        method = CapturePayment.build(payment_id=payment_id)
        params = method.build_params(
            amount=amount,
            receipt=receipt,
            airline=airline,
            transfers=transfers,
            deal=deal
        )
        headers = {'Idempotence-Key': self._get_idempotence_key()}
        result = await self._client._send_request(method, json=params, headers=headers)
        return Payment(**result)

    async def cancel_payment(self, payment_id: str) -> Payment:
        method = CancelPayment.build(payment_id=payment_id)
        headers = {'Idempotence-Key': self._get_idempotence_key()}
        result = await self._client._send_request(method, headers=headers)
        return Payment(**result)

    @staticmethod
    def _get_idempotence_key() -> str:
        return str(uuid.uuid4())

