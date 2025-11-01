from typing import List, Optional

from pydantic import BaseModel

from .payment import PaymentAmount


class AccountStatus:
    """Account status values."""

    ENABLED = "enabled"
    DISABLED = "disabled"


class Fiscalization(BaseModel):
    """
    Fiscalization settings
    """

    enabled: bool
    provider: str
    fiscalization_enabled: Optional[bool] = None


class Settings(BaseModel):
    """
    Settings object for shop or gateway (Me)

    Contains actual information about the settings of the requested shop or gateway.
    """

    account_id: str
    status: str  # enabled or disabled
    test: bool
    fiscalization: Optional[Fiscalization] = None
    payment_methods: Optional[List[str]] = None
    itn: Optional[str] = None
    payout_methods: Optional[List[str]] = None
    name: Optional[str] = None
    payout_balance: Optional[PaymentAmount] = None
