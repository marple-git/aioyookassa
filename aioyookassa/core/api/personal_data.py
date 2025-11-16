from typing import Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.personal_data import CreatePersonalData, GetPersonalData
from aioyookassa.types.params import (
    CreatePersonalDataParams,
    PayoutStatementRecipientData,
    SbpPayoutRecipientData,
)
from aioyookassa.types.personal_data import PersonalData


class PersonalDataAPI(BaseAPI[CreatePersonalDataParams, PersonalData]):
    """
    YooKassa personal data API client.

    Provides methods for creating and retrieving personal data.
    """

    async def create_personal_data(
        self,
        params: CreatePersonalDataParams,
    ) -> PersonalData:
        """
        Create personal data in YooKassa.

        :param params: Personal data creation parameters (CreatePersonalDataParams).
        :type params: CreatePersonalDataParams
        :returns: PersonalData object.
        :rtype: PersonalData
        :seealso: https://yookassa.ru/developers/api#create_personal_data

        Example:
            >>> from aioyookassa.types.params import SbpPayoutRecipientData
            >>> params = SbpPayoutRecipientData(
            ...     last_name="Ivanov",
            ...     first_name="Ivan",
            ...     middle_name="Ivanovich"
            ... )
            >>> personal_data = await client.personal_data.create_personal_data(params)
        """
        return await self._create_resource(
            params=params,
            params_class=CreatePersonalDataParams,  # type: ignore[arg-type]
            method_class=CreatePersonalData,
            result_class=PersonalData,
        )

    async def get_personal_data(self, personal_data_id: str) -> PersonalData:
        """
        Retrieve personal data information by personal data ID.

        :param personal_data_id: Personal data identifier.
        :type personal_data_id: str
        :returns: PersonalData object.
        :rtype: PersonalData
        :seealso: https://yookassa.ru/developers/api#get_personal_data
        """
        return await self._get_by_id(
            resource_id=personal_data_id,
            method_class=GetPersonalData,
            result_class=PersonalData,
            id_param_name="personal_data_id",
        )
