from typing import Optional, Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.invoices import CreateInvoice, GetInvoice
from aioyookassa.types.invoice import Invoice
from aioyookassa.types.params import CreateInvoiceParams


class InvoicesAPI(BaseAPI[CreateInvoiceParams, Invoice]):
    """
    YooKassa invoices API client.

    Provides methods for creating and retrieving invoice information.
    Note: YooKassa API does not support listing all invoices.
    """

    async def create_invoice(
        self,
        params: CreateInvoiceParams,
    ) -> Invoice:
        """
        Create a new invoice in YooKassa.

        :param params: Invoice creation parameters (CreateInvoiceParams).
        :type params: CreateInvoiceParams
        :returns: Invoice object.
        :rtype: Invoice
        :seealso: https://yookassa.ru/developers/api#create_invoice

        Example:
            >>> from aioyookassa.types.params import CreateInvoiceParams
            >>> from aioyookassa.types.invoice import InvoicePaymentData, InvoiceCartItem
            >>> params = CreateInvoiceParams(
            ...     payment_data=InvoicePaymentData(...),
            ...     cart=[InvoiceCartItem(...)],
            ...     expires_at="2024-12-31T23:59:59Z"
            ... )
            >>> invoice = await client.invoices.create_invoice(params)
        """
        return await self._create_resource(
            params=params,
            params_class=CreateInvoiceParams,
            method_class=CreateInvoice,
            result_class=Invoice,
        )

    async def get_invoice(self, invoice_id: str) -> Invoice:
        """
        Retrieve invoice information by invoice ID.

        :param invoice_id: Invoice identifier.
        :type invoice_id: str
        :returns: Invoice object.
        :rtype: Invoice
        :seealso: https://yookassa.ru/developers/api#get_invoice
        """
        return await self._get_by_id(
            resource_id=invoice_id,
            method_class=GetInvoice,
            result_class=Invoice,
            id_param_name="invoice_id",
        )
