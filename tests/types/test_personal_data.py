"""
Tests for personal data types.
"""

import datetime
from datetime import date

import pytest

from aioyookassa.types.enum import (
    PersonalDataCancellationParty,
    PersonalDataCancellationReason,
    PersonalDataStatus,
    PersonalDataType,
)
from aioyookassa.types.personal_data import (
    PersonalData,
    PersonalDataCancellationDetails,
)


class TestPersonalDataCancellationDetails:
    """Test PersonalDataCancellationDetails model."""

    def test_personal_data_cancellation_details_creation(self):
        """Test PersonalDataCancellationDetails creation."""
        details = PersonalDataCancellationDetails(
            party=PersonalDataCancellationParty.YOO_MONEY,
            reason=PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT,
        )
        assert details.party == PersonalDataCancellationParty.YOO_MONEY
        assert details.reason == PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT


class TestPersonalData:
    """Test PersonalData model."""

    def test_personal_data_creation_minimal(self):
        """Test PersonalData creation with minimal fields."""
        personal_data = PersonalData(
            id="pd_123456789",
            type=PersonalDataType.SBP_PAYOUT_RECIPIENT,
            status=PersonalDataStatus.WAITING_FOR_OPERATION,
            created_at=datetime.datetime.now(),
        )
        assert personal_data.id == "pd_123456789"
        assert personal_data.type == PersonalDataType.SBP_PAYOUT_RECIPIENT
        assert personal_data.status == PersonalDataStatus.WAITING_FOR_OPERATION
        assert personal_data.cancellation_details is None
        assert personal_data.expires_at is None
        assert personal_data.metadata is None

    def test_personal_data_creation_full(self):
        """Test PersonalData creation with all fields."""
        cancellation_details = PersonalDataCancellationDetails(
            party=PersonalDataCancellationParty.YOO_MONEY,
            reason=PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT,
        )

        personal_data = PersonalData(
            id="pd_123456789",
            type=PersonalDataType.PAYOUT_STATEMENT_RECIPIENT,
            status=PersonalDataStatus.ACTIVE,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=30),
            cancellation_details=cancellation_details,
            metadata={"key": "value"},
        )
        assert personal_data.id == "pd_123456789"
        assert personal_data.type == PersonalDataType.PAYOUT_STATEMENT_RECIPIENT
        assert personal_data.status == PersonalDataStatus.ACTIVE
        assert personal_data.expires_at is not None
        assert personal_data.cancellation_details == cancellation_details
        assert personal_data.metadata == {"key": "value"}

    def test_personal_data_with_different_types(self):
        """Test PersonalData with different type values."""
        types = [
            PersonalDataType.SBP_PAYOUT_RECIPIENT,
            PersonalDataType.PAYOUT_STATEMENT_RECIPIENT,
        ]

        for data_type in types:
            personal_data = PersonalData(
                id="pd_123456789",
                type=data_type,
                status=PersonalDataStatus.WAITING_FOR_OPERATION,
                created_at=datetime.datetime.now(),
            )
            assert personal_data.type == data_type

    def test_personal_data_with_different_statuses(self):
        """Test PersonalData with different status values."""
        statuses = [
            PersonalDataStatus.WAITING_FOR_OPERATION,
            PersonalDataStatus.ACTIVE,
            PersonalDataStatus.CANCELED,
        ]

        for status in statuses:
            personal_data = PersonalData(
                id="pd_123456789",
                type=PersonalDataType.SBP_PAYOUT_RECIPIENT,
                status=status,
                created_at=datetime.datetime.now(),
            )
            assert personal_data.status == status

    def test_personal_data_with_active_status_and_expires_at(self):
        """Test PersonalData with ACTIVE status and expires_at."""
        expires_at = datetime.datetime.now() + datetime.timedelta(days=30)

        personal_data = PersonalData(
            id="pd_123456789",
            type=PersonalDataType.SBP_PAYOUT_RECIPIENT,
            status=PersonalDataStatus.ACTIVE,
            created_at=datetime.datetime.now(),
            expires_at=expires_at,
        )
        assert personal_data.status == PersonalDataStatus.ACTIVE
        assert personal_data.expires_at == expires_at

    def test_personal_data_with_canceled_status(self):
        """Test PersonalData with CANCELED status and cancellation_details."""
        cancellation_details = PersonalDataCancellationDetails(
            party=PersonalDataCancellationParty.YOO_MONEY,
            reason=PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT,
        )

        personal_data = PersonalData(
            id="pd_123456789",
            type=PersonalDataType.SBP_PAYOUT_RECIPIENT,
            status=PersonalDataStatus.CANCELED,
            created_at=datetime.datetime.now(),
            cancellation_details=cancellation_details,
        )
        assert personal_data.status == PersonalDataStatus.CANCELED
        assert personal_data.cancellation_details == cancellation_details
