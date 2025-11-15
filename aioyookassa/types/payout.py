import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .enum import Currency, PayoutStatus, SelfEmployedStatus
from .payment import CancellationDetails, Deal, PaymentAmount


class PayoutCardInfo(BaseModel):
    """
    Bank card information for payout
    """

    first6: str
    last4: str
    card_type: str
    issuer_country: Optional[str] = None
    issuer_name: Optional[str] = None


class BankCardPayoutDestination(BaseModel):
    """
    Bank card payout destination
    """

    type: str = "bank_card"
    card: PayoutCardInfo


class SbpPayoutDestination(BaseModel):
    """
    SBP (Fast Payments System) payout destination
    """

    type: str = "sbp"
    bank_id: str
    phone: str
    recipient_checked: bool


class YooMoneyPayoutDestination(BaseModel):
    """
    YooMoney wallet payout destination
    """

    type: str = "yoo_money"
    account_number: str


# Union type for payout destinations
PayoutDestination = Union[
    BankCardPayoutDestination, SbpPayoutDestination, YooMoneyPayoutDestination
]


class PayoutReceipt(BaseModel):
    """
    Receipt data for self-employed payout
    """

    service_name: str
    npd_receipt_id: Optional[str] = None
    url: Optional[str] = None
    amount: Optional[PaymentAmount] = None


class SelfEmployedConfirmation(BaseModel):
    """
    Self-employed confirmation object
    """

    type: str = "redirect"
    confirmation_url: str


class SelfEmployed(BaseModel):
    """
    Self-employed person data

    Can be used in two contexts:
    1. In Payout object - only id is required
    2. In SelfEmployed API responses - all fields except itn, phone, confirmation are required
    """

    id: str
    status: Optional[SelfEmployedStatus] = None
    created_at: Optional[datetime.datetime] = None
    itn: Optional[str] = None
    phone: Optional[str] = None
    confirmation: Optional[SelfEmployedConfirmation] = None
    test: Optional[bool] = None


class Payout(BaseModel):
    """
    Payout object
    """

    id: str
    amount: PaymentAmount
    status: PayoutStatus
    payout_destination: PayoutDestination
    description: Optional[str] = None
    created_at: datetime.datetime
    succeeded_at: Optional[datetime.datetime] = None
    deal: Optional[Deal] = None
    self_employed: Optional[SelfEmployed] = None
    receipt: Optional[PayoutReceipt] = None
    cancellation_details: Optional[CancellationDetails] = None
    metadata: Optional[dict] = None
    test: bool
