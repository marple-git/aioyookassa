from typing import Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.self_employed import CreateSelfEmployed, GetSelfEmployed
from aioyookassa.types.params import CreateSelfEmployedParams
from aioyookassa.types.payout import SelfEmployed


class SelfEmployedAPI(BaseAPI[CreateSelfEmployedParams, SelfEmployed]):
    """
    YooKassa self-employed API client.

    Provides methods for creating and retrieving self-employed persons.
    """

    async def create_self_employed(
        self,
        params: CreateSelfEmployedParams,
    ) -> SelfEmployed:
        """
        Create a new self-employed in YooKassa.

        :param params: Self-employed creation parameters (CreateSelfEmployedParams).
        :type params: CreateSelfEmployedParams
        :returns: SelfEmployed object.
        :rtype: SelfEmployed
        :seealso: https://yookassa.ru/developers/api#create_self_employed

        Example:
            >>> from aioyookassa.types.params import (
            ...     CreateSelfEmployedParams,
            ...     SelfEmployedConfirmationData
            ... )
            >>> params = CreateSelfEmployedParams(
            ...     itn="123456789012",
            ...     confirmation=SelfEmployedConfirmationData(
            ...         confirmation_url="https://example.com/confirm"
            ...     )
            ... )
            >>> self_employed = await client.self_employed.create_self_employed(params)
        """
        return await self._create_resource(
            params=params,
            params_class=CreateSelfEmployedParams,
            method_class=CreateSelfEmployed,
            result_class=SelfEmployed,
        )

    async def get_self_employed(self, self_employed_id: str) -> SelfEmployed:
        """
        Retrieve self-employed information by self-employed ID.

        :param self_employed_id: Self-employed identifier.
        :type self_employed_id: str
        :returns: SelfEmployed object.
        :rtype: SelfEmployed
        :seealso: https://yookassa.ru/developers/api#get_self_employed
        """
        return await self._get_by_id(
            resource_id=self_employed_id,
            method_class=GetSelfEmployed,
            result_class=SelfEmployed,
            id_param_name="self_employed_id",
        )
