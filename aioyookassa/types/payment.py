import datetime
from typing import Union, Optional, List

from pydantic import BaseModel, Field

from .enum import PaymentStatus, ReceiptRegistration, CancellationParty, CancellationReason, ConfirmationType


class Confirmation(BaseModel):
    """
    Confirmation
    """
    type: ConfirmationType
    enforce: Optional[bool] = None
    locale: Optional[str] = None
    return_url: Optional[str] = None
    url: Optional[str] = Field(None, alias='confirmation_url')


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
    kpp: Optional[str] = None


class VatData(BaseModel):
    """
    VAT data
    """
    type: str
    amount: Optional[PaymentAmount] = None
    rate: Optional[str] = None


class CardInfo(BaseModel):
    """
    Card information
    """
    first_six: Optional[str] = Field(None, alias='first6')
    last_four: str = Field(..., alias='last4')
    expiry_year: str
    expiry_month: str
    card_type: str
    card_country: Optional[str] = Field(None, alias='issuer_country')
    bank_name: Optional[str] = Field(None, alias='issuer_name')
    source: Optional[str] = None


class PaymentMethod(BaseModel):
    """
    Payment method
    """
    type: str
    id: str
    saved: bool
    title: Optional[str] = None
    login: Optional[str] = None
    card: Optional[CardInfo] = None
    phone: Optional[str] = None
    payer_bank_details: Optional[PayerBankDetails] = None
    payment_purpose: Optional[str] = None
    vat_data: Optional[VatData] = None
    account_number: Optional[str] = None


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
    description: Optional[str] = None
    metadata: Optional[dict] = None


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
    income_amount: Optional[PaymentAmount] = None
    description: Optional[str] = None
    recipient: Recipient
    payment_method: Optional[PaymentMethod] = None
    captured_at: Optional[datetime.datetime] = None
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime] = None
    confirmation: Optional[Confirmation] = None
    test: bool
    refunded_amount: Optional[PaymentAmount] = None
    paid: bool
    refundable: bool
    receipt_registration: Optional[ReceiptRegistration] = None
    metadata: Optional[dict] = None
    cancellation_details: Optional[CancellationDetails] = None
    authorization_details: Optional[AuthorizationDetails] = None
    transfers: Optional[List[Transfer]] = None
    deal: Optional[Deal] = None
    merchant_customer_id: Optional[str] = None


class PaymentsList(BaseModel):
    """
    Payments list
    """
    list: List[Payment] = Field(None, alias='items')
    cursor: Optional[str] = None


class Customer(BaseModel):
    """
    Customer
    """
    full_name: Optional[str] = None
    inn: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class MarkQuantity(BaseModel):
    """
    Mark quantity
    """
    numerator: int
    denominator: int


class MarkCodeInfo(BaseModel):
    """
    Mark code information
    """
    code: Optional[str] = Field(None, alias='mark_code_raw')
    unknown: Optional[str] = None
    ean_8: Optional[str] = None
    ean_13: Optional[str] = None
    itf_14: Optional[str] = None
    gs_10: Optional[str] = None
    gs_1m: Optional[str] = None
    short: Optional[str] = None
    fur: Optional[str] = None
    egais_20: Optional[str] = None
    egais_30: Optional[str] = None


class IndustryDetails(BaseModel):
    """
    Industry details
    """
    federal_id: str
    document_date: datetime.datetime
    document_number: str
    value: str


class PaymentItem(BaseModel):
    """
    Payment items
    """
    description: str
    amount: PaymentAmount
    vat_code: int
    quantity: str
    measure: Optional[str] = None
    mark_quantity: Optional[MarkQuantity] = None
    payment_subject: Optional[str] = None
    payment_mode: Optional[str] = None
    country_of_origin_code: Optional[str] = None
    customs_declaration_number: Optional[str] = None
    excise: Optional[str] = None
    product_code: Optional[str] = None
    mark_code_info: Optional[MarkCodeInfo] = None
    mark_mode: Optional[str] = None
    payment_subject_industry_details: Optional[IndustryDetails] = None


class OperationDetails(BaseModel):
    """
    Operation details
    """
    id: int = Field(..., alias='operation_id')
    value: str
    created_at: datetime.datetime


class Receipt(BaseModel):
    """
    Receipt
    """
    customer: Optional[Customer] = None
    items: List[PaymentItem]
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_system_code: Optional[int] = None
    receipt_industry_details: Optional[IndustryDetails] = None
    receipt_operation_details: Optional[OperationDetails] = None


class Passenger(BaseModel):
    first_name: str
    last_name: str


class Flight(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_date: datetime.datetime
    carrier_code: Optional[str] = None


class Airline(BaseModel):
    """
    Airline
    """
    ticket_number: Optional[str] = None
    booking_reference: Optional[str] = None
    passengers: Optional[List[Passenger]] = None
    flights: Optional[List[Flight]] = Field(None, alias='legs')
