from datetime import datetime
from typing import Any, List, Optional, Union

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods.invoices import CreateInvoice, GetInvoice
from aioyookassa.core.utils import generate_idempotence_key
from aioyookassa.types.invoice import (
    Invoice,
    InvoiceCartItem,
    InvoiceDeliveryMethodData,
    InvoicePaymentData,
)


class InvoicesAPI:
    """
    YooKassa invoices API client.

    Provides methods for creating and retrieving invoice information.
    Note: YooKassa API does not support listing all invoices.
    """

    def __init__(self, client: BaseAPIClient):
        self._client = client

    async def create_invoice(
        self,
        payment_data: InvoicePaymentData,
        cart: List[InvoiceCartItem],
        expires_at: Union[str, datetime],
        delivery_method_data: Optional[InvoiceDeliveryMethodData] = None,
        locale: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Invoice:
        """
        Create a new invoice in YooKassa.

        :param payment_data: Payment data for the invoice.
        :type payment_data: InvoicePaymentData
        :param cart: Cart items for the invoice.
        :type cart: List[InvoiceCartItem]
        :param expires_at: Invoice expiration date and time (ISO 8601 string or datetime object).
        :type expires_at: Union[str, datetime]
        :param delivery_method_data: Delivery method data.
        :type delivery_method_data: Optional[InvoiceDeliveryMethodData]
        :param locale: Interface language (ru_RU, en_US).
        :type locale: Optional[str]
        :param description: Invoice description (max 128 characters).
        :type description: Optional[str]
        :param metadata: Additional metadata.
        :type metadata: Optional[dict]
        :returns: Invoice object.
        :rtype: Invoice
        :seealso: https://yookassa.ru/developers/api#create_invoice
        """
        params = CreateInvoice.build_params(**locals())
        headers = {"Idempotence-Key": generate_idempotence_key()}
        result = await self._client._send_request(
            CreateInvoice, json=params, headers=headers
        )
        return Invoice(**result)

    async def get_invoice(self, invoice_id: str) -> Invoice:
        """
        Retrieve invoice information by invoice ID.

        :param invoice_id: Invoice identifier.
        :type invoice_id: str
        :returns: Invoice object.
        :rtype: Invoice
        :seealso: https://yookassa.ru/developers/api#get_invoice
        """
        method = GetInvoice.build(invoice_id=invoice_id)
        result = await self._client._send_request(method)
        return Invoice(**result)
