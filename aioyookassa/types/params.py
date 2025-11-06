"""
Pydantic models for API method parameters.
"""

from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import BaseModel

from aioyookassa.types.payment import Confirmation
from aioyookassa.types.enum import (
    PaymentMethodType,
    PaymentStatus,
    ReceiptStatus,
    ReceiptType,
)
from aioyookassa.types.invoice import (
    InvoiceCartItem,
    InvoiceDeliveryMethodData,
    InvoicePaymentData,
)
from aioyookassa.types.payment import (
    Airline,
    Customer,
    Deal,
    IndustryDetails,
    OperationDetails,
    PaymentAmount,
    PaymentMethod,
    Receipt,
    Recipient,
    Settlement,
    Transfer,
)
from aioyookassa.types.receipt_registration import (
    AdditionalUserProps,
    ReceiptRegistrationItem,
)
from aioyookassa.types.refund import RefundDeal, RefundMethod, RefundSource


# Payments API Parameters
class CreatePaymentParams(BaseModel):
    """Parameters for creating a payment."""

    amount: PaymentAmount
    description: Optional[str] = None
    receipt: Optional[Receipt] = None
    recipient: Optional[Recipient] = None
    payment_token: Optional[str] = None
    payment_method_id: Optional[str] = None
    payment_method_data: Optional[PaymentMethod] = None
    confirmation: Optional[Confirmation] = None
    save_payment_method: Optional[bool] = False
    capture: Optional[bool] = False
    client_ip: Optional[str] = None
    metadata: Optional[Any] = None
    airline: Optional[Airline] = None
    transfers: Optional[List[Transfer]] = None
    deal: Optional[Deal] = None
    merchant_customer_id: Optional[str] = None


class CapturePaymentParams(BaseModel):
    """Parameters for capturing a payment."""

    amount: Optional[PaymentAmount] = None
    receipt: Optional[Receipt] = None
    airline: Optional[Airline] = None
    transfers: Optional[List[Transfer]] = None
    deal: Optional[Deal] = None


class GetPaymentsParams(BaseModel):
    """Parameters for getting payments list."""

    created_at: Optional[datetime] = None
    captured_at: Optional[datetime] = None
    payment_method: Optional[PaymentMethodType] = None
    status: Optional[PaymentStatus] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


# Refunds API Parameters
class CreateRefundParams(BaseModel):
    """Parameters for creating a refund."""

    payment_id: str
    amount: PaymentAmount
    description: Optional[str] = None
    receipt: Optional[Receipt] = None
    sources: Optional[List[RefundSource]] = None
    deal: Optional[RefundDeal] = None
    refund_method_data: Optional[RefundMethod] = None


class GetRefundsParams(BaseModel):
    """Parameters for getting refunds list."""

    created_at_gte: Optional[datetime] = None
    created_at_gt: Optional[datetime] = None
    created_at_lte: Optional[datetime] = None
    created_at_lt: Optional[datetime] = None
    payment_id: Optional[str] = None
    status: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


# Invoices API Parameters
class CreateInvoiceParams(BaseModel):
    """Parameters for creating an invoice."""

    payment_data: InvoicePaymentData
    cart: List[InvoiceCartItem]
    expires_at: Union[str, datetime]
    delivery_method_data: Optional[InvoiceDeliveryMethodData] = None
    locale: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None


# Receipts API Parameters
class CreateReceiptParams(BaseModel):
    """Parameters for creating a receipt."""

    type: Union[ReceiptType, str]
    customer: Customer
    items: List[ReceiptRegistrationItem]
    settlements: List[Settlement]
    payment_id: Optional[str] = None
    refund_id: Optional[str] = None
    send: bool = True
    internet: Optional[bool] = None
    tax_system_code: Optional[int] = None
    timezone: Optional[int] = None
    additional_user_props: Optional[AdditionalUserProps] = None
    receipt_industry_details: Optional[List[IndustryDetails]] = None
    receipt_operational_details: Optional[OperationDetails] = None
    on_behalf_of: Optional[str] = None


class GetReceiptsParams(BaseModel):
    """Parameters for getting receipts list."""

    created_at_gte: Optional[datetime] = None
    created_at_gt: Optional[datetime] = None
    created_at_lte: Optional[datetime] = None
    created_at_lt: Optional[datetime] = None
    payment_id: Optional[str] = None
    refund_id: Optional[str] = None
    status: Optional[Union[ReceiptStatus, str]] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


# Payment Methods API Parameters
class PaymentMethodCardData(BaseModel):
    """Bank card data for payment method creation."""

    number: str
    expiry_year: str  # Format: YYYY
    expiry_month: str  # Format: MM
    cardholder: Optional[str] = None
    csc: Optional[str] = None  # CVC2 or CVV2 code


class PaymentMethodHolder(BaseModel):
    """Holder data for payment method creation."""

    gateway_id: str


class PaymentMethodConfirmation(BaseModel):
    """Confirmation data for payment method creation."""

    type: str  # Usually "redirect"
    enforce: Optional[bool] = None
    locale: Optional[str] = None
    return_url: str


class CreatePaymentMethodParams(BaseModel):
    """Parameters for creating a payment method."""

    type: str  # Required, e.g., "bank_card"
    card: Optional[PaymentMethodCardData] = None
    holder: Optional[PaymentMethodHolder] = None
    client_ip: Optional[str] = None
    confirmation: Optional[PaymentMethodConfirmation] = None
