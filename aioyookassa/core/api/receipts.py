from datetime import datetime
from typing import List, Optional, Union

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods.receipts import CreateReceipt, GetReceipt, GetReceipts
from aioyookassa.core.utils import generate_idempotence_key
from aioyookassa.types.enum import ReceiptStatus, ReceiptType
from aioyookassa.types.payment import Customer, IndustryDetails, OperationDetails
from aioyookassa.types.receipt_registration import (
    AdditionalUserProps,
    FiscalReceipt,
    FiscalReceiptsList,
    ReceiptRegistrationItem,
    ReceiptSettlement,
)


class ReceiptsAPI:
    """
    YooKassa receipts API client.

    Provides methods for creating, retrieving, and listing receipt registrations.
    """

    def __init__(self, client: BaseAPIClient):
        self._client = client

    async def create_receipt(
        self,
        type: Union[ReceiptType, str],
        customer: Customer,
        items: List[ReceiptRegistrationItem],
        settlements: List[ReceiptSettlement],
        payment_id: Optional[str] = None,
        refund_id: Optional[str] = None,
        send: bool = True,
        internet: Optional[bool] = None,
        tax_system_code: Optional[int] = None,
        timezone: Optional[int] = None,
        additional_user_props: Optional[AdditionalUserProps] = None,
        receipt_industry_details: Optional[List[IndustryDetails]] = None,
        receipt_operational_details: Optional[OperationDetails] = None,
        on_behalf_of: Optional[str] = None,
    ) -> FiscalReceipt:
        """
        Create a new receipt registration.

        :param type: Receipt type (ReceiptType.PAYMENT or ReceiptType.REFUND).
        :param customer: Customer information.
        :param items: Receipt items.
        :param settlements: List of settlements.
        :param payment_id: Payment ID (required for payment receipts).
        :param refund_id: Refund ID (required for refund receipts).
        :param send: Send receipt immediately (always True).
        :param internet: Internet payment flag.
        :param tax_system_code: Tax system code.
        :param timezone: Timezone number.
        :param additional_user_props: Additional user properties.
        :param receipt_industry_details: Industry details.
        :param receipt_operational_details: Operational details.
        :param on_behalf_of: Shop ID for split payments.
        :return: FiscalReceipt object.
        :seealso: https://yookassa.ru/developers/api#create_receipt
        """
        params = CreateReceipt.build_params(**locals())
        headers = {"Idempotence-Key": generate_idempotence_key()}
        result = await self._client._send_request(
            CreateReceipt, json=params, headers=headers
        )
        return FiscalReceipt(**result)

    async def get_receipts(
        self,
        created_at_gte: Optional[datetime] = None,
        created_at_gt: Optional[datetime] = None,
        created_at_lte: Optional[datetime] = None,
        created_at_lt: Optional[datetime] = None,
        payment_id: Optional[str] = None,
        refund_id: Optional[str] = None,
        status: Optional[Union[ReceiptStatus, str]] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        **kwargs,
    ) -> FiscalReceiptsList:
        """
        Retrieve a list of receipt registrations with optional filtering.

        :param created_at_gte: Creation date greater than or equal.
        :param created_at_gt: Creation date greater than.
        :param created_at_lte: Creation date less than or equal.
        :param created_at_lt: Creation date less than.
        :param payment_id: Filter by payment ID.
        :param refund_id: Filter by refund ID.
        :param status: Receipt status (ReceiptStatus.PENDING, ReceiptStatus.SUCCEEDED, ReceiptStatus.CANCELED).
        :param limit: Maximum number of records.
        :param cursor: Pagination cursor.
        :param kwargs: Additional parameters.
        :return: FiscalReceiptsList object.
        :seealso: https://yookassa.ru/developers/api#get_receipts_list
        """
        params = GetReceipts.build_params(
            created_at_gte=created_at_gte,
            created_at_gt=created_at_gt,
            created_at_lte=created_at_lte,
            created_at_lt=created_at_lt,
            payment_id=payment_id,
            refund_id=refund_id,
            status=status,
            limit=limit,
            cursor=cursor,
            **kwargs,
        )
        result = await self._client._send_request(GetReceipts, params=params)
        return FiscalReceiptsList(**result)

    async def get_receipt(self, receipt_id: str) -> FiscalReceipt:
        """
        Retrieve receipt registration information by receipt ID.

        :param receipt_id: Receipt identifier.
        :return: FiscalReceipt object.
        :seealso: https://yookassa.ru/developers/api#get_receipt
        """
        method = GetReceipt.build(receipt_id=receipt_id)
        result = await self._client._send_request(method)
        return FiscalReceipt(**result)
