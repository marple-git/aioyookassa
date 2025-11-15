import datetime
from typing import Optional

from pydantic import BaseModel

from .enum import (
    PersonalDataCancellationParty,
    PersonalDataCancellationReason,
    PersonalDataStatus,
    PersonalDataType,
)


class PersonalDataCancellationDetails(BaseModel):
    """
    Cancellation details for personal data
    """

    party: PersonalDataCancellationParty
    reason: PersonalDataCancellationReason


class PersonalData(BaseModel):
    """
    Personal data object
    """

    id: str
    type: PersonalDataType
    status: PersonalDataStatus
    created_at: datetime.datetime
    cancellation_details: Optional[PersonalDataCancellationDetails] = None
    expires_at: Optional[datetime.datetime] = None
    metadata: Optional[dict] = None
