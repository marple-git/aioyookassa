"""
Tests for self-employed types.
"""

import datetime

import pytest

from aioyookassa.types.enum import SelfEmployedStatus
from aioyookassa.types.payout import SelfEmployed, SelfEmployedConfirmation


class TestSelfEmployedConfirmation:
    """Test SelfEmployedConfirmation model."""

    def test_self_employed_confirmation_creation(self):
        """Test SelfEmployedConfirmation creation."""
        confirmation = SelfEmployedConfirmation(
            confirmation_url="https://example.com/confirm"
        )
        assert confirmation.type == "redirect"
        assert confirmation.confirmation_url == "https://example.com/confirm"

    def test_self_employed_confirmation_with_explicit_type(self):
        """Test SelfEmployedConfirmation with explicit type."""
        confirmation = SelfEmployedConfirmation(
            type="redirect", confirmation_url="https://example.com/confirm"
        )
        assert confirmation.type == "redirect"
        assert confirmation.confirmation_url == "https://example.com/confirm"


class TestSelfEmployed:
    """Test SelfEmployed model."""

    def test_self_employed_creation_minimal(self):
        """Test SelfEmployed creation with minimal fields (for use in Payout)."""
        self_employed = SelfEmployed(id="se_123456789")
        assert self_employed.id == "se_123456789"
        assert self_employed.status is None
        assert self_employed.created_at is None
        assert self_employed.test is None

    def test_self_employed_creation_full(self):
        """Test SelfEmployed creation with all fields."""
        confirmation = SelfEmployedConfirmation(
            confirmation_url="https://example.com/confirm"
        )

        self_employed = SelfEmployed(
            id="se_123456789",
            status=SelfEmployedStatus.CONFIRMED,
            created_at=datetime.datetime.now(),
            itn="123456789012",
            phone="79000000000",
            confirmation=confirmation,
            test=True,
        )
        assert self_employed.id == "se_123456789"
        assert self_employed.status == SelfEmployedStatus.CONFIRMED
        assert self_employed.created_at is not None
        assert self_employed.itn == "123456789012"
        assert self_employed.phone == "79000000000"
        assert self_employed.confirmation == confirmation
        assert self_employed.test is True

    def test_self_employed_with_optional_fields(self):
        """Test SelfEmployed with optional fields."""
        self_employed = SelfEmployed(
            id="se_123456789",
            status=SelfEmployedStatus.PENDING,
            created_at=datetime.datetime.now(),
            test=False,
        )
        assert self_employed.id == "se_123456789"
        assert self_employed.status == SelfEmployedStatus.PENDING
        assert self_employed.itn is None
        assert self_employed.phone is None
        assert self_employed.confirmation is None

    def test_self_employed_with_different_statuses(self):
        """Test SelfEmployed with different status values."""
        statuses = [
            SelfEmployedStatus.PENDING,
            SelfEmployedStatus.CONFIRMED,
            SelfEmployedStatus.CANCELED,
            SelfEmployedStatus.UNREGISTERED,
        ]

        for status in statuses:
            self_employed = SelfEmployed(
                id="se_123456789",
                status=status,
                created_at=datetime.datetime.now(),
                test=True,
            )
            assert self_employed.status == status
