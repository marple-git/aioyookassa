from aioyookassa.core.api.base import BaseAPI, _EmptyParams
from aioyookassa.core.methods.sbp_banks import GetSbpBanks
from aioyookassa.types.sbp_banks import SbpBanksList


class SbpBanksAPI(BaseAPI[_EmptyParams, SbpBanksList]):
    """
    YooKassa SBP banks API client.

    Provides methods for retrieving SBP participant banks list.
    """

    async def get_sbp_banks(self) -> SbpBanksList:
        """
        Retrieve list of SBP participant banks.

        :returns: SbpBanksList object.
        :rtype: SbpBanksList
        :seealso: https://yookassa.ru/developers/api#get_sbp_banks

        Example:
            >>> banks = await client.sbp_banks.get_sbp_banks()
            >>> for bank in banks.list:
            ...     print(f"{bank.name} (BIC: {bank.bic})")
        """
        return await self._get_list(
            params=None,
            params_class=None,
            method_class=GetSbpBanks,
            result_class=SbpBanksList,
        )
