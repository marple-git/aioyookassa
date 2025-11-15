"""
Pydantic models for API method parameters.
"""

from datetime import date, datetime
from typing import Any, List, Optional, Union

from pydantic import BaseModel

from .enum import (
    DealStatus,
    FeeMoment,
    PaymentMethodType,
    PaymentStatus,
    ReceiptStatus,
    ReceiptType,
)
from .invoice import InvoiceCartItem, InvoiceDeliveryMethodData, InvoicePaymentData
from .payment import (
    Airline,
    Confirmation,
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
from .payout import SelfEmployed, SelfEmployedConfirmation
from .receipt_registration import AdditionalUserProps, ReceiptRegistrationItem
from .refund import RefundDeal, RefundMethod, RefundSource


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


# Payouts API Parameters
class BankCardPayoutCardData(BaseModel):
    """Bank card number for payout creation."""

    number: str


class BankCardPayoutDestinationData(BaseModel):
    """Bank card data for payout creation."""

    type: str = "bank_card"
    card: BankCardPayoutCardData


class SbpPayoutDestinationData(BaseModel):
    """SBP payout destination data for payout creation."""

    type: str = "sbp"
    bank_id: str
    phone: str


class YooMoneyPayoutDestinationData(BaseModel):
    """YooMoney payout destination data for payout creation."""

    type: str = "yoo_money"
    account_number: str


PayoutDestinationData = Union[
    BankCardPayoutDestinationData,
    SbpPayoutDestinationData,
    YooMoneyPayoutDestinationData,
]


class PayoutReceiptData(BaseModel):
    """Receipt data for self-employed payout creation."""

    service_name: str
    amount: Optional[PaymentAmount] = None


class CreatePayoutParams(BaseModel):
    """Parameters for creating a payout."""

    amount: PaymentAmount
    payout_destination_data: Optional[PayoutDestinationData] = None
    payout_token: Optional[str] = None
    payment_method_id: Optional[str] = None
    description: Optional[str] = None
    deal: Optional[Deal] = None
    self_employed: Optional[SelfEmployed] = None
    receipt_data: Optional[PayoutReceiptData] = None
    personal_data: Optional[List[str]] = None
    metadata: Optional[dict] = None


# Self-Employed API Parameters
class SelfEmployedConfirmationData(BaseModel):
    """Confirmation data for self-employed creation."""

    type: str = "redirect"
    confirmation_url: str


class CreateSelfEmployedParams(BaseModel):
    """Parameters for creating a self-employed."""

    itn: Optional[str] = None
    phone: Optional[str] = None
    confirmation: Optional[SelfEmployedConfirmationData] = None


# Personal Data API Parameters
class SbpPayoutRecipientData(BaseModel):
    """Data for sbp_payout_recipient type personal data."""

    type: str = "sbp_payout_recipient"
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    metadata: Optional[dict] = None


class PayoutStatementRecipientData(BaseModel):
    """Data for payout_statement_recipient type personal data."""

    type: str = "payout_statement_recipient"
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    birthdate: Union[str, date, datetime]  # ISO 8601 format
    metadata: Optional[dict] = None


CreatePersonalDataParams = Union[SbpPayoutRecipientData, PayoutStatementRecipientData]


# Deals API Parameters
class CreateDealParams(BaseModel):
    """Parameters for creating a deal."""

    type: str = "safe_deal"
    fee_moment: FeeMoment
    metadata: Optional[dict] = None
    description: Optional[str] = None


class GetDealsParams(BaseModel):
    """Parameters for getting deals list."""

    created_at_gte: Optional[datetime] = None
    created_at_gt: Optional[datetime] = None
    created_at_lte: Optional[datetime] = None
    created_at_lt: Optional[datetime] = None
    expires_at_gte: Optional[datetime] = None
    expires_at_gt: Optional[datetime] = None
    expires_at_lte: Optional[datetime] = None
    expires_at_lt: Optional[datetime] = None
    status: Optional[Union[DealStatus, str]] = None
    full_text_search: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


# Webhooks API Parameters
class CreateWebhookParams(BaseModel):
    """Parameters for creating a webhook."""

    event: str
    url: str
