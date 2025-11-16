from typing import Any, Optional, Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.payments import (
    CancelPayment,
    CapturePayment,
    CreatePayment,
    GetPayment,
    GetPayments,
)
from aioyookassa.types import Payment, PaymentsList
from aioyookassa.types.params import (
    CapturePaymentParams,
    CreatePaymentParams,
    GetPaymentsParams,
)


class PaymentsAPI(BaseAPI[CreatePaymentParams, Payment]):
    """
    YooKassa payments API client.

    Provides methods for creating, retrieving, capturing, and canceling payments.
    """

    async def create_payment(
        self,
        params: CreatePaymentParams,
    ) -> Payment:
        """
        Create a new payment in YooKassa.

        :param params: Payment creation parameters (CreatePaymentParams).
        :type params: CreatePaymentParams
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#create_payment

        Example:
            >>> from aioyookassa.types.params import CreatePaymentParams
            >>> from aioyookassa.types.payment import PaymentAmount
            >>> from aioyookassa.types.enum import Currency
            >>> params = CreatePaymentParams(
            ...     amount=PaymentAmount(value=100.00, currency=Currency.RUB),
            ...     description="Test payment"
            ... )
            >>> payment = await client.payments.create_payment(params)
        """
        return await self._create_resource(
            params=params,
            params_class=CreatePaymentParams,
            method_class=CreatePayment,
            result_class=Payment,
        )

    async def get_payments(
        self,
        params: Optional[GetPaymentsParams] = None,
        **kwargs: Any,
    ) -> PaymentsList:
        """
        Retrieve a list of payments with optional filtering.

        :param params: Filter parameters (GetPaymentsParams).
        :type params: Optional[GetPaymentsParams]
        :param kwargs: Additional parameters (merged with params).
        :returns: Payments list object.
        :rtype: PaymentsList
        :seealso: https://yookassa.ru/developers/api#list_payments

        Example:
            >>> from aioyookassa.types.params import GetPaymentsParams
            >>> from aioyookassa.types.enum import PaymentStatus
            >>> params = GetPaymentsParams(status=PaymentStatus.SUCCEEDED, limit=10)
            >>> payments = await client.payments.get_payments(params)
        """
        return await self._get_list(
            params=params,
            params_class=GetPaymentsParams,
            method_class=GetPayments,
            result_class=PaymentsList,
            **kwargs,
        )

    async def get_payment(self, payment_id: str) -> Payment:
        """
        Retrieve payment information by payment ID.

        :param payment_id: Payment identifier.
        :type payment_id: str
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#get_payment
        """
        return await self._get_by_id(
            resource_id=payment_id,
            method_class=GetPayment,
            result_class=Payment,
            id_param_name="payment_id",
        )

    async def capture_payment(
        self,
        payment_id: str,
        params: Optional[CapturePaymentParams] = None,
    ) -> Payment:
        """
        Capture (confirm) a payment.

        :param payment_id: Payment identifier.
        :type payment_id: str
        :param params: Capture parameters (CapturePaymentParams).
        :type params: Optional[CapturePaymentParams]
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#capture_payment

        Example:
            >>> from aioyookassa.types.params import CapturePaymentParams
            >>> params = CapturePaymentParams(amount=PaymentAmount(value=100.00, currency=Currency.RUB))
            >>> payment = await client.payments.capture_payment("payment_id", params)
        """
        return await self._update_resource(
            resource_id=payment_id,
            params=params,
            params_class=CapturePaymentParams,
            method_class=CapturePayment,
            result_class=Payment,
            id_param_name="payment_id",
        )

    async def cancel_payment(self, payment_id: str) -> Payment:
        """
        Cancel a payment by its identifier.

        :param payment_id: Payment identifier.
        :type payment_id: str
        :returns: Payment object.
        :rtype: Payment
        :seealso: https://yookassa.ru/developers/api#cancel_payment
        """
        return await self._action_resource(
            resource_id=payment_id,
            method_class=CancelPayment,
            result_class=Payment,
            id_param_name="payment_id",
        )
