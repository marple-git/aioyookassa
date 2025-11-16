from typing import Any, Optional, Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.refunds import CreateRefund, GetRefund, GetRefunds
from aioyookassa.types.params import CreateRefundParams, GetRefundsParams
from aioyookassa.types.refund import Refund, RefundsList


class RefundsAPI(BaseAPI[CreateRefundParams, Refund]):
    """
    YooKassa refunds API client.

    Provides methods for creating, retrieving, and listing refunds.
    """

    async def create_refund(
        self,
        params: CreateRefundParams,
    ) -> Refund:
        """
        Create a new refund for a successful payment.

        :param params: Refund creation parameters (CreateRefundParams).
        :type params: CreateRefundParams
        :returns: Refund object.
        :rtype: Refund
        :seealso: https://yookassa.ru/developers/api#create_refund

        Example:
            >>> from aioyookassa.types.params import CreateRefundParams
            >>> from aioyookassa.types.payment import PaymentAmount
            >>> params = CreateRefundParams(
            ...     payment_id="payment_id",
            ...     amount=PaymentAmount(value=100.00, currency=Currency.RUB)
            ... )
            >>> refund = await client.refunds.create_refund(params)
        """
        return await self._create_resource(
            params=params,
            params_class=CreateRefundParams,
            method_class=CreateRefund,
            result_class=Refund,
        )

    async def get_refunds(
        self,
        params: Optional[GetRefundsParams] = None,
        **kwargs: Any,
    ) -> RefundsList:
        """
        Retrieve a list of refunds with optional filtering.

        :param params: Filter parameters (GetRefundsParams).
        :type params: Optional[GetRefundsParams]
        :param kwargs: Additional parameters (merged with params).
        :returns: Refunds list object.
        :rtype: RefundsList
        :seealso: https://yookassa.ru/developers/api#get_refunds_list

        Example:
            >>> from aioyookassa.types.params import GetRefundsParams
            >>> params = GetRefundsParams(status="succeeded", limit=10)
            >>> refunds = await client.refunds.get_refunds(params)
        """
        return await self._get_list(
            params=params,
            params_class=GetRefundsParams,
            method_class=GetRefunds,
            result_class=RefundsList,
            **kwargs,
        )

    async def get_refund(self, refund_id: str) -> Refund:
        """
        Retrieve refund information by refund ID.

        :param refund_id: Refund identifier.
        :type refund_id: str
        :returns: Refund object.
        :rtype: Refund
        :seealso: https://yookassa.ru/developers/api#get_refund
        """
        return await self._get_by_id(
            resource_id=refund_id,
            method_class=GetRefund,
            result_class=Refund,
            id_param_name="refund_id",
        )
