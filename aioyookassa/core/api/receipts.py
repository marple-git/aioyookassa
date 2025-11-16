from typing import Any, Optional, Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.receipts import CreateReceipt, GetReceipt, GetReceipts
from aioyookassa.types.params import CreateReceiptParams, GetReceiptsParams
from aioyookassa.types.receipt_registration import FiscalReceipt, FiscalReceiptsList


class ReceiptsAPI(BaseAPI[CreateReceiptParams, FiscalReceipt]):
    """
    YooKassa receipts API client.

    Provides methods for creating, retrieving, and listing receipt registrations.
    """

    async def create_receipt(
        self,
        params: CreateReceiptParams,
    ) -> FiscalReceipt:
        """
        Create a new receipt registration.

        :param params: Receipt creation parameters (CreateReceiptParams).
        :type params: CreateReceiptParams
        :returns: FiscalReceipt object.
        :rtype: FiscalReceipt
        :seealso: https://yookassa.ru/developers/api#create_receipt

        Example:
            >>> from aioyookassa.types.params import CreateReceiptParams
            >>> from aioyookassa.types.enum import ReceiptType
            >>> params = CreateReceiptParams(
            ...     type=ReceiptType.PAYMENT,
            ...     customer=Customer(...),
            ...     items=[...],
            ...     settlements=[...]
            ... )
            >>> receipt = await client.receipts.create_receipt(params)
        """
        return await self._create_resource(
            params=params,
            params_class=CreateReceiptParams,
            method_class=CreateReceipt,
            result_class=FiscalReceipt,
        )

    async def get_receipts(
        self,
        params: Optional[GetReceiptsParams] = None,
        **kwargs: Any,
    ) -> FiscalReceiptsList:
        """
        Retrieve a list of receipt registrations with optional filtering.

        :param params: Filter parameters (GetReceiptsParams).
        :type params: Optional[GetReceiptsParams]
        :param kwargs: Additional parameters (merged with params).
        :returns: FiscalReceiptsList object.
        :rtype: FiscalReceiptsList
        :seealso: https://yookassa.ru/developers/api#get_receipts_list

        Example:
            >>> from aioyookassa.types.params import GetReceiptsParams
            >>> from aioyookassa.types.enum import ReceiptStatus
            >>> params = GetReceiptsParams(status=ReceiptStatus.SUCCEEDED, limit=10)
            >>> receipts = await client.receipts.get_receipts(params)
        """
        return await self._get_list(
            params=params,
            params_class=GetReceiptsParams,
            method_class=GetReceipts,
            result_class=FiscalReceiptsList,
            **kwargs,
        )

    async def get_receipt(self, receipt_id: str) -> FiscalReceipt:
        """
        Retrieve receipt registration information by receipt ID.

        :param receipt_id: Receipt identifier.
        :return: FiscalReceipt object.
        :seealso: https://yookassa.ru/developers/api#get_receipt
        """
        return await self._get_by_id(
            resource_id=receipt_id,
            method_class=GetReceipt,
            result_class=FiscalReceipt,
            id_param_name="receipt_id",
        )
