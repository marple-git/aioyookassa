from typing import Any, Optional, Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.deals import CreateDeal, GetDeal, GetDeals
from aioyookassa.types.deals import Deal, DealsList
from aioyookassa.types.params import CreateDealParams, GetDealsParams


class DealsAPI(BaseAPI[CreateDealParams, Deal]):
    """
    YooKassa deals API client.

    Provides methods for creating and retrieving deals.
    """

    async def create_deal(
        self,
        params: CreateDealParams,
    ) -> Deal:
        """
        Create a new deal in YooKassa.

        :param params: Deal creation parameters (CreateDealParams).
        :type params: CreateDealParams
        :returns: Deal object.
        :rtype: Deal
        :seealso: https://yookassa.ru/developers/api#create_deal
        """
        return await self._create_resource(
            params=params,
            params_class=CreateDealParams,
            method_class=CreateDeal,
            result_class=Deal,
        )

    async def get_deals(
        self,
        params: Optional[GetDealsParams] = None,
        **kwargs: Any,
    ) -> DealsList:
        """
        Retrieve a list of deals with optional filtering.

        :param params: Filter parameters (GetDealsParams).
        :type params: Optional[GetDealsParams]
        :param kwargs: Additional parameters (merged with params).
        :returns: Deals list object.
        :rtype: DealsList
        :seealso: https://yookassa.ru/developers/api#list_deals
        """
        return await self._get_list(
            params=params,
            params_class=GetDealsParams,
            method_class=GetDeals,
            result_class=DealsList,
            **kwargs,
        )

    async def get_deal(self, deal_id: str) -> Deal:
        """
        Retrieve deal information by deal ID.

        :param deal_id: Deal identifier.
        :type deal_id: str
        :returns: Deal object.
        :rtype: Deal
        :seealso: https://yookassa.ru/developers/api#get_deal
        """
        return await self._get_by_id(
            resource_id=deal_id,
            method_class=GetDeal,
            result_class=Deal,
            id_param_name="deal_id",
        )
