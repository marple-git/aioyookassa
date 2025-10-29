# This file has been refactored. See core/payments/api.py for PaymentsAPI implementation.

from datetime import datetime
from typing import Any, List, Optional

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods.payments import (
    CancelPayment,
    CapturePayment,
    CreatePayment,
    GetPayment,
    GetPayments,
)
from aioyookassa.core.utils import generate_idempotence_key
from aioyookassa.types import Confirmation, Payment, PaymentsList
from aioyookassa.types.enum import PaymentMethodType, PaymentStatus
from aioyookassa.types.payment import (
    Airline,
    Deal,
    PaymentAmount,
    PaymentMethod,
    Receipt,
    Recipient,
    Transfer,
)


class PaymentsAPI:
    """
    YooKassa payments API client.

    Provides methods for creating, retrieving, capturing, and canceling payments.
    """

    def __init__(self, client: BaseAPIClient):
        self._client = client

    async def create_payment(
        self,
        amount: PaymentAmount,
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
        merchant_customer_id: Optional[str] = None,
    ) -> Payment:
        """
        Create a new payment in YooKassa.

        :param amount: Payment amount.
        :type amount: PaymentAmount
        :param description: Payment description.
        :type description: Optional[str]
        :param receipt: Receipt data.
        :type receipt: Optional[Receipt]
        :param recipient: Payment recipient.
        :type recipient: Optional[Recipient]
        :param payment_token: Payment token.
        :type payment_token: Optional[str]
        :param payment_method_id: Payment method ID.
        :type payment_method_id: Optional[str]
        :param payment_method_data: Payment method data.
        :type payment_method_data: Optional[PaymentMethod]
        :param confirmation: Confirmation method.
        :type confirmation: Optional[Confirmation]
        :param save_payment_method: Save payment method flag.
        :type save_payment_method: Optional[bool]
        :param capture: Capture payment immediately flag.
        :type capture: Optional[bool]
        :param client_ip: Client IP address.
        :type client_ip: Optional[str]
        :param metadata: Additional metadata.
        :type metadata: Optional[Any]
        :param airline: Airline data.
        :type airline: Optional[Airline]
        :param transfers: Transfers list.
        :type transfers: Optional[List[Transfer]]
        :param deal: Deal data.
        :type deal: Optional[Deal]
        :param merchant_customer_id: Merchant customer ID.
        :type merchant_customer_id: Optional[str]
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#create_payment
        """
        params = CreatePayment.build_params(**locals())
        headers = {"Idempotence-Key": generate_idempotence_key()}
        result = await self._client._send_request(
            CreatePayment, json=params, headers=headers
        )
        return Payment(**result)

    async def get_payments(
        self,
        created_at: Optional[datetime] = None,
        captured_at: Optional[datetime] = None,
        payment_method: Optional[PaymentMethodType] = None,
        status: Optional[PaymentStatus] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        **kwargs: Any,
    ) -> PaymentsList:
        """
        Retrieve a list of payments with optional filtering.

        :param created_at: Creation date.
        :type created_at: Optional[datetime]
        :param captured_at: Capture date.
        :type captured_at: Optional[datetime]
        :param payment_method: Payment method type.
        :type payment_method: Optional[PaymentMethodType]
        :param status: Payment status.
        :type status: Optional[PaymentStatus]
        :param limit: Maximum number of records.
        :type limit: Optional[int]
        :param cursor: Pagination cursor.
        :type cursor: Optional[str]
        :param kwargs: Additional parameters.
        :returns: Payments list object.
        :rtype: PaymentsList
        :seealso: https://yookassa.ru/developers/api#list_payments
        """
        params = GetPayments.build_params(
            created_at=created_at,
            captured_at=captured_at,
            payment_method=payment_method,
            status=status,
            limit=limit,
            cursor=cursor,
            **kwargs,
        )
        result = await self._client._send_request(GetPayments, params=params)
        return PaymentsList(**result)

    async def get_payment(self, payment_id: str) -> Payment:
        """
        Retrieve payment information by payment ID.

        :param payment_id: Payment identifier.
        :type payment_id: str
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#get_payment
        """
        method = GetPayment.build(payment_id=payment_id)
        result = await self._client._send_request(method)
        return Payment(**result)

    async def capture_payment(
        self,
        payment_id: str,
        amount: Optional[PaymentAmount] = None,
        receipt: Optional[Receipt] = None,
        airline: Optional[Airline] = None,
        transfers: Optional[List[Transfer]] = None,
        deal: Optional[Deal] = None,
    ) -> Payment:
        """
        Capture (confirm) a payment.

        :param payment_id: Payment identifier.
        :type payment_id: str
        :param amount: Payment amount.
        :type amount: Optional[PaymentAmount]
        :param receipt: Receipt data.
        :type receipt: Optional[Receipt]
        :param airline: Airline data.
        :type airline: Optional[Airline]
        :param transfers: Transfers list.
        :type transfers: Optional[List[Transfer]]
        :param deal: Deal data.
        :type deal: Optional[Deal]
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#capture_payment
        """
        method = CapturePayment.build(payment_id=payment_id)
        params = method.build_params(
            amount=amount,
            receipt=receipt,
            airline=airline,
            transfers=transfers,
            deal=deal,
        )
        headers = {"Idempotence-Key": generate_idempotence_key()}
        result = await self._client._send_request(method, json=params, headers=headers)
        return Payment(**result)

    async def cancel_payment(self, payment_id: str) -> Payment:
        """
        Cancel a payment by its identifier.

        :param payment_id: Payment identifier.
        :type payment_id: str
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#cancel_payment
        """
        method = CancelPayment.build(payment_id=payment_id)
        headers = {"Idempotence-Key": generate_idempotence_key()}
        result = await self._client._send_request(method, headers=headers)
        return Payment(**result)
