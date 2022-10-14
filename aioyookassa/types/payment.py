import datetime
from typing import Union, Optional, List

from pydantic import BaseModel, Field

from .enum import PaymentStatus, ReceiptRegistration, CancellationParty, CancellationReason


class Confirmation(BaseModel):
    """
    Confirmation
    """
    type: str = 'redirect'
    enforce: Optional[bool] = None
    locale: Optional[str] = None
    return_url: Optional[str]


class PaymentAmount(BaseModel):
    """
    Payment amount
    """
    value: Union[int, float]
    currency: str


class Recipient(BaseModel):
    """
    Payment receiver
    """
    account_id: str
    gateway_id: str


class PayerBankDetails(BaseModel):
    """
    Bank details of the payer
    """
    full_name: str
    short_name: str
    address: str
    inn: str
    bank_name: str
    bank_branch: str
    bank_bik: str
    bank_account: str
    kpp: Optional[str]


class VatData(BaseModel):
    """
    VAT data
    """
    type: str
    amount: Optional[PaymentAmount]
    rate: Optional[str]


class CardInfo(BaseModel):
    """
    Card information
    """
    first_six: Optional[str]
    last_four: str
    expiry_year: str
    expiry_month: str
    card_type: str


class PaymentMethod(BaseModel):
    """
    Payment method
    """
    type: str
    id: str
    saved: bool
    title: Optional[str]
    login: Optional[str]
    card: Optional[CardInfo]
    phone: Optional[str]
    payer_bank_details: Optional[PayerBankDetails]
    payment_purpose: Optional[str]
    vat_data: Optional[VatData]
    account_number: Optional[str]


class CancellationDetails(BaseModel):
    party: CancellationParty
    reason: CancellationReason


class ThreeDSInfo(BaseModel):
    """
    3DS information
    """
    applied: bool


class AuthorizationDetails(BaseModel):
    transaction_identifier: str = Field(None, alias='rrn')
    authorization_code: str = Field(None, alias='auth_code')
    three_d_secure: ThreeDSInfo


class Transfer(BaseModel):
    account_id: str
    amount: PaymentAmount
    status: PaymentStatus
    fee_amount: PaymentAmount = Field(None, alias='platform_fee_amount')
    description: Optional[str]
    metadata: Optional[dict]


class Settlement(BaseModel):
    type: str
    amount: PaymentAmount


class Deal(BaseModel):
    id: str
    settlements: List[PaymentAmount]


class Payment(BaseModel):
    """
    Payment
    """
    id: str
    status: PaymentStatus
    amount: PaymentAmount
    income_amount: Optional[PaymentAmount]
    description: Optional[str]
    recipient: Recipient
    payment_method: Optional[PaymentMethod]
    captured_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime]
    confirmation: Optional[Confirmation]
    test: bool
    refunded_amount: Optional[PaymentAmount]
    paid: bool
    refundable: bool
    receipt_registration: Optional[ReceiptRegistration]
    metadata: Optional[dict]
    cancellation_details: Optional[CancellationDetails]
    authorization_details: Optional[AuthorizationDetails]
    transfers: Optional[List[Transfer]]
    deal: Optional[Deal]
    merchant_customer_id: Optional[str]
