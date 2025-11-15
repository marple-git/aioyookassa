"""
Tests for SBP banks types.
"""

import pytest

from aioyookassa.types.sbp_banks import SbpBanksList, SbpParticipantBank


class TestSbpParticipantBank:
    """Test SbpParticipantBank model."""

    def test_sbp_participant_bank_creation(self):
        """Test SbpParticipantBank creation."""
        bank = SbpParticipantBank(
            bank_id="100000000001", name="Test Bank", bic="044525225"
        )
        assert bank.bank_id == "100000000001"
        assert bank.name == "Test Bank"
        assert bank.bic == "044525225"

    def test_sbp_participant_bank_with_different_values(self):
        """Test SbpParticipantBank with different values."""
        bank = SbpParticipantBank(
            bank_id="100000000002", name="Another Bank", bic="044525226"
        )
        assert bank.bank_id == "100000000002"
        assert bank.name == "Another Bank"
        assert bank.bic == "044525226"


class TestSbpBanksList:
    """Test SbpBanksList model."""

    def test_sbp_banks_list_creation(self):
        """Test SbpBanksList creation."""
        bank1 = SbpParticipantBank(
            bank_id="100000000001", name="Test Bank 1", bic="044525225"
        )
        bank2 = SbpParticipantBank(
            bank_id="100000000002", name="Test Bank 2", bic="044525226"
        )
        banks_list = SbpBanksList(items=[bank1, bank2])
        assert len(banks_list.list) == 2
        assert banks_list.list[0] == bank1
        assert banks_list.list[1] == bank2

    def test_sbp_banks_list_with_alias(self):
        """Test SbpBanksList with alias field."""
        bank_data = {
            "bank_id": "100000000001",
            "name": "Test Bank",
            "bic": "044525225",
        }
        banks_data = {"items": [bank_data]}
        banks_list = SbpBanksList(**banks_data)
        assert len(banks_list.list) == 1
        assert banks_list.list[0].bank_id == "100000000001"
        assert banks_list.list[0].name == "Test Bank"
        assert banks_list.list[0].bic == "044525225"

    def test_sbp_banks_list_empty(self):
        """Test SbpBanksList with empty list."""
        banks_list = SbpBanksList(items=[])
        assert len(banks_list.list) == 0

    def test_sbp_banks_list_with_none(self):
        """Test SbpBanksList with None items."""
        banks_list = SbpBanksList(items=None)
        assert banks_list.list is None
