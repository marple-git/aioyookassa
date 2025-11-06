import datetime
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .enum import ReceiptRegistration
from .payment import CancellationDetails, Deal, PaymentAmount, Receipt, Settlement


class RefundSource(BaseModel):
    """
    Refund source for split payments.
    """

    account_id: str
    amount: PaymentAmount
    platform_fee_amount: Optional[PaymentAmount] = None


class RefundDeal(BaseModel):
    """
    Refund deal - данные о сделке
    """

    id: str
    refund_settlements: List[Settlement]


class RefundArticle(BaseModel):
    """
    Refund article for electronic certificate refund cart.
    """

    article_number: int
    payment_article_number: int
    tru_code: str
    quantity: Union[int, float, str, Decimal]


class ElectronicCertificateData(BaseModel):
    """
    Electronic certificate data.
    """

    amount: PaymentAmount
    basket_id: str


class RefundMethod(BaseModel):
    """
    Refund method details.
    """

    type: str
    sbp_operation_id: Optional[str] = None  # for SBP
    articles: Optional[List[RefundArticle]] = None  # for electronic certificate
    electronic_certificate: Optional[ElectronicCertificateData] = None


class RefundAuthorizationDetails(BaseModel):
    """
    Refund authorization details.
    """

    rrn: Optional[str] = None  # Retrieval Reference Number


class Refund(BaseModel):
    """
    Refund.
    """

    id: str
    payment_id: str
    status: str
    amount: PaymentAmount
    created_at: datetime.datetime
    description: Optional[str] = None
    cancellation_details: Optional[CancellationDetails] = None
    receipt_registration: Optional[ReceiptRegistration] = None
    sources: Optional[List[RefundSource]] = None
    deal: Optional[RefundDeal] = None
    refund_method: Optional[RefundMethod] = None
    refund_authorization_details: Optional[RefundAuthorizationDetails] = None


class RefundsList(BaseModel):
    """
    Refunds list.
    """

    list: Optional[List[Refund]] = Field(None, alias="items")
    next_cursor: Optional[str] = None
