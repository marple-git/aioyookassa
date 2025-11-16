from typing import Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.payouts import CreatePayout, GetPayout
from aioyookassa.types.params import CreatePayoutParams
from aioyookassa.types.payout import Payout


class PayoutsAPI(BaseAPI[CreatePayoutParams, Payout]):
    """
    YooKassa payouts API client.

    Provides methods for creating and retrieving payouts.
    """

    async def create_payout(
        self,
        params: CreatePayoutParams,
    ) -> Payout:
        """
        Create a new payout in YooKassa.

        :param params: Payout creation parameters (CreatePayoutParams).
        :type params: CreatePayoutParams
        :returns: Payout object.
        :rtype: Payout
        :seealso: https://yookassa.ru/developers/api#create_payout

        Example:
            >>> from aioyookassa.types.params import CreatePayoutParams
            >>> from aioyookassa.types.payment import PaymentAmount
            >>> from aioyookassa.types.enum import Currency
            >>> params = CreatePayoutParams(
            ...     amount=PaymentAmount(value=100.00, currency=Currency.RUB),
            ...     payout_destination_data=BankCardPayoutDestinationData(
            ...         card={"number": "5555555555554477"}
            ...     )
            ... )
            >>> payout = await client.payouts.create_payout(params)
        """
        return await self._create_resource(
            params=params,
            params_class=CreatePayoutParams,
            method_class=CreatePayout,
            result_class=Payout,
        )

    async def get_payout(self, payout_id: str) -> Payout:
        """
        Retrieve payout information by payout ID.

        :param payout_id: Payout identifier.
        :type payout_id: str
        :returns: Payout object.
        :rtype: Payout
        :seealso: https://yookassa.ru/developers/api#get_payout
        """
        return await self._get_by_id(
            resource_id=payout_id,
            method_class=GetPayout,
            result_class=Payout,
            id_param_name="payout_id",
        )
