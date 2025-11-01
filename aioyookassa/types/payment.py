import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, model_validator

from .enum import (
    CancellationParty,
    CancellationReason,
    ConfirmationType,
    Currency,
    PaymentMethodStatus,
    PaymentMode,
    PaymentStatus,
    PaymentSubject,
    ReceiptRegistration,
)


class Confirmation(BaseModel):
    """
    Confirmation

    Validation rules by type:
    - embedded: requires confirmation_token
    - external: no additional fields required
    - mobile_application: requires confirmation_url (url)
    - qr: requires confirmation_data
    - redirect: requires confirmation_url (url)
    """

    type: ConfirmationType
    enforce: Optional[bool] = None
    locale: Optional[str] = None
    return_url: Optional[str] = None
    confirmation_token: Optional[str] = None
    confirmation_data: Optional[str] = None
    url: Optional[str] = Field(None, alias="confirmation_url")

    @model_validator(mode="before")
    @classmethod
    def validate_confirmation_fields(cls, data: Any) -> Any:
        """
        Validate that required fields are present based on confirmation type.
        """
        if isinstance(data, dict):
            # Normalize: if 'url' is provided, map it to 'confirmation_url' (the alias)
            if "url" in data and "confirmation_url" not in data:
                data["confirmation_url"] = data["url"]

            confirmation_type = data.get("type")

            # Handle both enum and string values
            if confirmation_type is not None and hasattr(confirmation_type, "value"):
                confirmation_type_value = confirmation_type.value
            elif isinstance(confirmation_type, str):
                confirmation_type_value = confirmation_type
            else:
                confirmation_type_value = (
                    str(confirmation_type) if confirmation_type else None
                )

            if (
                confirmation_type_value == ConfirmationType.EMBEDDED
                or confirmation_type_value == "embedded"
            ):
                if not data.get("confirmation_token"):
                    raise ValueError(
                        f"confirmation_token is required for type 'embedded'"
                    )

            elif (
                confirmation_type_value == ConfirmationType.MOBILE_APPLICATION
                or confirmation_type_value == "mobile_application"
            ):
                if not data.get("confirmation_url"):
                    raise ValueError(
                        f"confirmation_url is required for type 'mobile_application'"
                    )

            elif (
                confirmation_type_value == ConfirmationType.QR_CODE
                or confirmation_type_value == "qr"
            ):
                if not data.get("confirmation_data"):
                    raise ValueError(f"confirmation_data is required for type 'qr'")

            elif (
                confirmation_type_value == ConfirmationType.REDIRECT
                or confirmation_type_value == "redirect"
            ):
                if not data.get("confirmation_url"):
                    raise ValueError(
                        f"confirmation_url is required for type 'redirect'"
                    )

        return data


class PaymentAmount(BaseModel):
    """
    Payment amount

    Supports multiple numeric types for convenience:
    - int: PaymentAmount(value=100, currency="RUB")
    - float: PaymentAmount(value=100.50, currency="RUB")
    - str: PaymentAmount(value="100.00", currency="RUB")
    - Decimal: PaymentAmount(value=Decimal("100.00"), currency="RUB")
    """

    value: Union[int, float, str, Decimal]
    currency: Union[Currency, str] = Currency.RUB


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

    full_name: Optional[str] = None
    short_name: Optional[str] = None
    address: Optional[str] = None
    inn: Optional[str] = None
    bank_name: Optional[str] = None
    bank_branch: Optional[str] = None
    bank_bik: Optional[str] = None
    bank_account: Optional[str] = None
    kpp: Optional[str] = None
    # SBP-specific fields
    bank_id: Optional[str] = None
    bic: Optional[str] = None
    sbp_operation_id: Optional[str] = None


class VatData(BaseModel):
    """
    VAT data
    """

    type: str
    amount: Optional[PaymentAmount] = None
    rate: Optional[str] = None


class CardProduct(BaseModel):
    """
    Card product information
    """

    code: str
    name: Optional[str] = None


class CardInfo(BaseModel):
    """
    Card information
    """

    first_six: Optional[str] = Field(None, alias="first6")
    last_four: str = Field(..., alias="last4")
    expiry_year: str
    expiry_month: str
    card_type: str
    card_product: Optional[CardProduct] = None
    card_country: Optional[str] = Field(None, alias="issuer_country")
    bank_name: Optional[str] = Field(None, alias="issuer_name")
    source: Optional[str] = None


class CertificateCompensation(BaseModel):
    """
    Certificate compensation information
    """

    value: Union[int, float, str, Decimal]
    currency: Union[Currency, str] = Currency.RUB


class Certificate(BaseModel):
    """
    Electronic certificate information
    """

    certificate_id: str
    tru_quantity: int
    available_compensation: CertificateCompensation
    applied_compensation: CertificateCompensation


class Article(BaseModel):
    """
    Article information for electronic certificate
    """

    article_number: int
    tru_code: str
    article_code: Optional[str] = None
    certificates: List[Certificate]


class PaymentMethod(BaseModel):
    """
    Payment method
    """

    type: str
    id: str
    saved: bool
    status: PaymentMethodStatus
    title: Optional[str] = None
    login: Optional[str] = None
    card: Optional[CardInfo] = None
    phone: Optional[str] = None
    payer_bank_details: Optional[PayerBankDetails] = None
    payment_purpose: Optional[str] = None
    vat_data: Optional[VatData] = None
    account_number: Optional[str] = None
    discount_amount: Optional[PaymentAmount] = None
    loan_option: Optional[str] = None
    suspended_until: Optional[datetime.datetime] = None
    # Electronic certificate fields
    articles: Optional[List[Article]] = None


class CancellationDetails(BaseModel):
    party: CancellationParty
    reason: CancellationReason


class ThreeDSInfo(BaseModel):
    """
    3DS information
    """

    applied: bool


class AuthorizationDetails(BaseModel):
    transaction_identifier: Optional[str] = Field(None, alias="rrn")
    authorization_code: Optional[str] = Field(None, alias="auth_code")
    three_d_secure: ThreeDSInfo


class Transfer(BaseModel):
    account_id: str
    amount: PaymentAmount
    status: PaymentStatus
    fee_amount: Optional[PaymentAmount] = Field(None, alias="platform_fee_amount")
    description: Optional[str] = None
    metadata: Optional[dict] = None


class Settlement(BaseModel):
    type: str
    amount: PaymentAmount


class Deal(BaseModel):
    id: str
    settlements: List[PaymentAmount]


class InvoiceDetails(BaseModel):
    """
    Invoice details
    """

    id: Optional[str] = None


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
    invoice_details: Optional[InvoiceDetails] = None


class PaymentsList(BaseModel):
    """
    Payments list
    """

    list: Optional[List[Payment]] = Field(None, alias="items")
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

    code: Optional[str] = Field(None, alias="mark_code_raw")
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
    quantity: Union[int, float, str, Decimal]
    payment_subject: PaymentSubject
    payment_mode: PaymentMode
    measure: Optional[str] = None
    mark_quantity: Optional[MarkQuantity] = None
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

    id: int = Field(..., alias="operation_id")
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
    internet: Optional[bool] = None
    timezone: Optional[int] = None
    receipt_industry_details: Optional[List[IndustryDetails]] = None
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
    flights: Optional[List[Flight]] = Field(None, alias="legs")
