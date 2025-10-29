import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .enum import Currency
from .payment import (
    Customer,
    IndustryDetails,
    MarkCodeInfo,
    MarkQuantity,
    OperationDetails,
    PaymentAmount,
    Recipient,
)


class InvoiceCartItem(BaseModel):
    """
    Invoice cart item.
    """

    description: str
    price: PaymentAmount
    discount_price: Optional[PaymentAmount] = None
    quantity: Union[int, float, str, Decimal]  # API accepts number (integer or decimal)


class InvoiceDeliveryMethodData(BaseModel):
    """
    Invoice delivery method data.
    """

    type: str  # self


class InvoiceReceiptItem(BaseModel):
    """
    Invoice receipt item.
    """

    description: str
    amount: PaymentAmount
    vat_code: int
    quantity: Union[int, float, str, Decimal]
    measure: Optional[str] = None
    mark_quantity: Optional[MarkQuantity] = None
    payment_subject: Optional[str] = None
    payment_mode: Optional[str] = None
    country_of_origin_code: Optional[str] = None
    customs_declaration_number: Optional[str] = None
    excise: Optional[str] = None
    product_code: Optional[str] = None
    planned_status: Optional[int] = None
    mark_code_info: Optional[MarkCodeInfo] = None
    mark_mode: Optional[str] = None
    payment_subject_industry_details: Optional[List[IndustryDetails]] = None


class InvoiceReceipt(BaseModel):
    """
    Invoice receipt data for fiscal receipt generation.
    """

    customer: Optional[Customer] = None
    items: List[InvoiceReceiptItem]
    internet: Optional[bool] = None
    tax_system_code: Optional[int] = None
    timezone: Optional[int] = None
    receipt_industry_details: Optional[List[IndustryDetails]] = None
    receipt_operational_details: Optional[OperationDetails] = None


class InvoicePaymentData(BaseModel):
    """
    Invoice payment data for processing payment by invoice.
    """

    amount: PaymentAmount
    receipt: Optional[InvoiceReceipt] = None
    recipient: Optional[Recipient] = None
    save_payment_method: Optional[bool] = None
    capture: Optional[bool] = None
    client_ip: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None


class Invoice(BaseModel):
    """
    Invoice.
    """

    id: str
    status: str
    cart: List[InvoiceCartItem]
    delivery_method_data: Optional[InvoiceDeliveryMethodData] = None
    payment_data: Optional[InvoicePaymentData] = None
    created_at: datetime.datetime
    expires_at: datetime.datetime
    locale: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None
    url: Optional[str] = None
