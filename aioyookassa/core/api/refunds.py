from datetime import datetime
from typing import Any, List, Optional

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods.refunds import CreateRefund, GetRefund, GetRefunds
from aioyookassa.core.utils import generate_idempotence_key
from aioyookassa.types.payment import PaymentAmount, Receipt
from aioyookassa.types.refund import (
    Refund,
    RefundDeal,
    RefundMethod,
    RefundsList,
    RefundSource,
)


class RefundsAPI:
    """
    YooKassa refunds API client.

    Provides methods for creating, retrieving, and listing refunds.
    """

    def __init__(self, client: BaseAPIClient):
        self._client = client

    async def create_refund(
        self,
        payment_id: str,
        amount: PaymentAmount,
        description: Optional[str] = None,
        receipt: Optional[Receipt] = None,
        sources: Optional[List[RefundSource]] = None,
        deal: Optional[RefundDeal] = None,
        refund_method_data: Optional[RefundMethod] = None,
    ) -> Refund:
        """
        Create a new refund for a successful payment.

        :param payment_id: Payment identifier.
        :type payment_id: str
        :param amount: Refund amount.
        :type amount: PaymentAmount
        :param description: Refund description/reason.
        :type description: Optional[str]
        :param receipt: Receipt data.
        :type receipt: Optional[Receipt]
        :param sources: Refund sources for split payments.
        :type sources: Optional[List[RefundSource]]
        :param deal: Deal data for safe deal.
        :type deal: Optional[RefundDeal]
        :param refund_method_data: Refund method details.
        :type refund_method_data: Optional[RefundMethod]
        :returns: Refund object.
        :rtype: Refund
        :seealso: https://yookassa.ru/developers/api#create_refund
        """
        params = CreateRefund.build_params(**locals())
        headers = {"Idempotence-Key": generate_idempotence_key()}
        result = await self._client._send_request(
            CreateRefund, json=params, headers=headers
        )
        return Refund(**result)

    async def get_refunds(
        self,
        created_at_gte: Optional[datetime] = None,
        created_at_gt: Optional[datetime] = None,
        created_at_lte: Optional[datetime] = None,
        created_at_lt: Optional[datetime] = None,
        payment_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        **kwargs,
    ) -> RefundsList:
        """
        Retrieve a list of refunds with optional filtering.

        :param created_at_gte: Creation date greater than or equal.
        :type created_at_gte: Optional[datetime]
        :param created_at_gt: Creation date greater than.
        :type created_at_gt: Optional[datetime]
        :param created_at_lte: Creation date less than or equal.
        :type created_at_lte: Optional[datetime]
        :param created_at_lt: Creation date less than.
        :type created_at_lt: Optional[datetime]
        :param payment_id: Filter by payment ID.
        :type payment_id: Optional[str]
        :param status: Refund status (pending, succeeded, canceled).
        :type status: Optional[str]
        :param limit: Maximum number of records.
        :type limit: Optional[int]
        :param cursor: Pagination cursor.
        :type cursor: Optional[str]
        :param kwargs: Additional parameters.
        :returns: Refunds list object.
        :rtype: RefundsList
        :seealso: https://yookassa.ru/developers/api#get_refunds_list
        """
        params = GetRefunds.build_params(
            created_at_gte=created_at_gte,
            created_at_gt=created_at_gt,
            created_at_lte=created_at_lte,
            created_at_lt=created_at_lt,
            payment_id=payment_id,
            status=status,
            limit=limit,
            cursor=cursor,
            **kwargs,
        )
        result = await self._client._send_request(GetRefunds, params=params)
        return RefundsList(**result)

    async def get_refund(self, refund_id: str) -> Refund:
        """
        Retrieve refund information by refund ID.

        :param refund_id: Refund identifier.
        :type refund_id: str
        :returns: Refund object.
        :rtype: Refund
        :seealso: https://yookassa.ru/developers/api#get_refund
        """
        method = GetRefund.build(refund_id=refund_id)
        result = await self._client._send_request(method)
        return Refund(**result)
