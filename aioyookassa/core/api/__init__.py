"""
YooKassa API clients.

This module contains all API client implementations for different YooKassa services.
"""

from .base import BaseAPI
from .deals import DealsAPI
from .invoices import InvoicesAPI
from .payment_methods import PaymentMethodsAPI
from .payments import PaymentsAPI
from .payouts import PayoutsAPI
from .personal_data import PersonalDataAPI
from .receipts import ReceiptsAPI
from .refunds import RefundsAPI
from .sbp_banks import SbpBanksAPI
from .self_employed import SelfEmployedAPI
from .webhooks import WebhooksAPI

__all__ = [
    "BaseAPI",
    "DealsAPI",
    "InvoicesAPI",
    "PaymentMethodsAPI",
    "PaymentsAPI",
    "PersonalDataAPI",
    "PayoutsAPI",
    "ReceiptsAPI",
    "RefundsAPI",
    "SbpBanksAPI",
    "SelfEmployedAPI",
    "WebhooksAPI",
]
