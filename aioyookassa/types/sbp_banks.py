from typing import List, Optional

from pydantic import BaseModel, Field


class SbpParticipantBank(BaseModel):
    """
    SBP participant bank object
    """

    bank_id: str
    name: str
    bic: str


class SbpBanksList(BaseModel):
    """
    SBP banks list
    """

    list: Optional[List[SbpParticipantBank]] = Field(None, alias="items")
