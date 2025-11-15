"""
Deal types for YooKassa API.
"""

import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .enum import DealStatus, FeeMoment
from .payment import PaymentAmount


class Deal(BaseModel):
    """
    Deal object for Safe Deal API

    Contains all information about a deal, current at the moment.
    It is created when a deal is created and comes in response to any request related to deals.
    """

    type: str = "safe_deal"
    id: str
    fee_moment: FeeMoment
    description: Optional[str] = None
    balance: PaymentAmount
    payout_balance: PaymentAmount
    status: DealStatus
    created_at: datetime.datetime
    expires_at: datetime.datetime
    metadata: Optional[dict] = None
    test: bool


class DealsList(BaseModel):
    """
    List of deals
    """

    list: Optional[List[Deal]] = Field(None, alias="items")
    next_cursor: Optional[str] = None
