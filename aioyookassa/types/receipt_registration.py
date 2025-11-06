import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel

from .enum import ReceiptStatus, ReceiptType
from .payment import (
    IndustryDetails,
    MarkCodeInfo,
    MarkQuantity,
    OperationDetails,
    PaymentAmount,
    Settlement,
)


class Supplier(BaseModel):
    """
    Supplier information.
    """

    name: Optional[str] = None
    phone: Optional[str] = None
    inn: Optional[str] = None


class ReceiptRegistrationItem(BaseModel):
    """
    Receipt registration item.
    """

    description: str
    quantity: Union[int, float, str, Decimal]
    amount: PaymentAmount
    vat_code: int
    payment_subject: Optional[str] = None
    payment_mode: Optional[str] = None
    country_of_origin_code: Optional[str] = None
    customs_declaration_number: Optional[str] = None
    excise: Optional[str] = None
    supplier: Optional[Supplier] = None
    agent_type: Optional[str] = None
    mark_code_info: Optional[MarkCodeInfo] = None
    measure: Optional[str] = None
    mark_quantity: Optional[MarkQuantity] = None
    payment_subject_industry_details: Optional[List[IndustryDetails]] = None
    product_code: Optional[str] = None
    planned_status: Optional[int] = None
    mark_mode: Optional[str] = None


class AdditionalUserProps(BaseModel):
    """
    Additional user properties.
    """

    name: str
    value: str


class FiscalReceipt(BaseModel):
    """
    Fiscal receipt.
    """

    id: str
    type: Union[ReceiptType, str]
    status: Union[ReceiptStatus, str]
    items: List[ReceiptRegistrationItem]
    payment_id: Optional[str] = None
    refund_id: Optional[str] = None
    fiscal_document_number: Optional[str] = None
    fiscal_storage_number: Optional[str] = None
    fiscal_attribute: Optional[str] = None
    registered_at: Optional[datetime.datetime] = None
    fiscal_provider_id: Optional[str] = None
    internet: Optional[bool] = None
    settlements: Optional[List[Settlement]] = None
    on_behalf_of: Optional[str] = None
    tax_system_code: Optional[int] = None
    timezone: Optional[int] = None
    receipt_industry_details: Optional[List[IndustryDetails]] = None
    receipt_operational_details: Optional[OperationDetails] = None


class FiscalReceiptsList(BaseModel):
    """
    Fiscal receipts list.
    """

    items: List[FiscalReceipt]
    next_cursor: Optional[str] = None
