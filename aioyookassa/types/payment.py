import datetime
from typing import Union, Optional, List

from pydantic import BaseModel, Field

from .enum import PaymentStatus, ReceiptRegistration, CancellationParty, CancellationReason, ConfirmationType


class Confirmation(BaseModel):
    """
    Confirmation
    """
    type: ConfirmationType
    enforce: Optional[bool]
    locale: Optional[str]
    return_url: Optional[str]
    confirmation_url: Optional[str]


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


class PaymentsList(BaseModel):
    """
    Payments list
    """
    list: List[Payment] = Field(None, alias='items')
    cursor: Optional[str]


class Customer(BaseModel):
    """
    Customer
    """
    full_name: Optional[str]
    inn: Optional[str]
    email: Optional[str]
    phone: Optional[str]


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
    unknown: Optional[str]
    ean_8: Optional[str]
    ean_13: Optional[str]
    itf_14: Optional[str]
    gs_10: Optional[str]
    gs_1m: Optional[str]
    short: Optional[str]
    fur: Optional[str]
    egais_20: Optional[str]
    egais_30: Optional[str]


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
    measure: Optional[str]
    mark_quantity: Optional[MarkQuantity]
    payment_subject: Optional[str]
    payment_mode: Optional[str]
    country_of_origin_code: Optional[str]
    customs_declaration_number: Optional[str]
    excise: Optional[str]
    product_code: Optional[str]
    mark_code_info: Optional[MarkCodeInfo]
    mark_mode: Optional[str]
    payment_subject_industry_details: Optional[IndustryDetails]


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
    customer: Optional[Customer]
    items: List[PaymentItem]
    phone: Optional[str]
    email: Optional[str]
    tax_system_code: Optional[int]
    receipt_industry_details: Optional[IndustryDetails]
    receipt_operation_details: Optional[OperationDetails]


class Passenger(BaseModel):
    first_name: str
    last_name: str


class Flight(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_date: datetime.datetime
    carrier_code: Optional[str]


class Airline(BaseModel):
    """
    Airline
    """
    ticket_number: Optional[str]
    booking_reference: Optional[str]
    passengers: Optional[List[Passenger]]
    flights: Optional[List[Flight]] = Field(None, alias='legs')
