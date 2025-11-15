"""
Tests for deal types.
"""

import datetime

import pytest

from aioyookassa.types.deals import Deal, DealsList
from aioyookassa.types.enum import Currency, DealStatus, FeeMoment
from aioyookassa.types.payment import PaymentAmount


class TestDeal:
    """Test Deal model."""

    def test_deal_creation_minimal(self):
        """Test Deal creation with minimal required fields."""
        deal = Deal(
            id="deal_123456789",
            fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
            balance=PaymentAmount(value=1000.00, currency=Currency.RUB),
            payout_balance=PaymentAmount(value=950.00, currency=Currency.RUB),
            status=DealStatus.OPENED,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
            test=True,
        )
        assert deal.type == "safe_deal"
        assert deal.id == "deal_123456789"
        assert deal.fee_moment == FeeMoment.PAYMENT_SUCCEEDED
        assert deal.balance.value == 1000.00
        assert deal.payout_balance.value == 950.00
        assert deal.status == DealStatus.OPENED
        assert deal.test is True
        assert deal.description is None
        assert deal.metadata is None

    def test_deal_creation_full(self):
        """Test Deal creation with all fields."""
        deal = Deal(
            id="deal_123456789",
            fee_moment=FeeMoment.DEAL_CLOSED,
            description="Test deal description",
            balance=PaymentAmount(value=2000.00, currency=Currency.RUB),
            payout_balance=PaymentAmount(value=1900.00, currency=Currency.RUB),
            status=DealStatus.CLOSED,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
            metadata={"order_id": "12345", "customer_id": "67890"},
            test=False,
        )
        assert deal.type == "safe_deal"
        assert deal.id == "deal_123456789"
        assert deal.fee_moment == FeeMoment.DEAL_CLOSED
        assert deal.description == "Test deal description"
        assert deal.balance.value == 2000.00
        assert deal.payout_balance.value == 1900.00
        assert deal.status == DealStatus.CLOSED
        assert deal.metadata == {"order_id": "12345", "customer_id": "67890"}
        assert deal.test is False

    def test_deal_with_different_statuses(self):
        """Test Deal with different status values."""
        statuses = [DealStatus.OPENED, DealStatus.CLOSED]

        for status in statuses:
            deal = Deal(
                id="deal_123456789",
                fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
                balance=PaymentAmount(value=1000.00, currency=Currency.RUB),
                payout_balance=PaymentAmount(value=950.00, currency=Currency.RUB),
                status=status,
                created_at=datetime.datetime.now(),
                expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
                test=True,
            )
            assert deal.status == status

    def test_deal_with_different_fee_moments(self):
        """Test Deal with different fee_moment values."""
        fee_moments = [FeeMoment.PAYMENT_SUCCEEDED, FeeMoment.DEAL_CLOSED]

        for fee_moment in fee_moments:
            deal = Deal(
                id="deal_123456789",
                fee_moment=fee_moment,
                balance=PaymentAmount(value=1000.00, currency=Currency.RUB),
                payout_balance=PaymentAmount(value=950.00, currency=Currency.RUB),
                status=DealStatus.OPENED,
                created_at=datetime.datetime.now(),
                expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
                test=True,
            )
            assert deal.fee_moment == fee_moment

    def test_deal_with_different_currencies(self):
        """Test Deal with different currencies."""
        currencies = [Currency.RUB, Currency.USD, Currency.EUR]

        for currency in currencies:
            deal = Deal(
                id="deal_123456789",
                fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
                balance=PaymentAmount(value=1000.00, currency=currency),
                payout_balance=PaymentAmount(value=950.00, currency=currency),
                status=DealStatus.OPENED,
                created_at=datetime.datetime.now(),
                expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
                test=True,
            )
            assert deal.balance.currency == currency
            assert deal.payout_balance.currency == currency


class TestDealsList:
    """Test DealsList model."""

    def test_deals_list_creation_empty(self):
        """Test DealsList creation with empty list."""
        deals_list = DealsList()
        assert deals_list.list is None
        assert deals_list.next_cursor is None

    def test_deals_list_creation_with_deals(self):
        """Test DealsList creation with deals."""
        deal1 = Deal(
            id="deal_123456789",
            fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
            balance=PaymentAmount(value=1000.00, currency=Currency.RUB),
            payout_balance=PaymentAmount(value=950.00, currency=Currency.RUB),
            status=DealStatus.OPENED,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
            test=True,
        )
        deal2 = Deal(
            id="deal_987654321",
            fee_moment=FeeMoment.DEAL_CLOSED,
            balance=PaymentAmount(value=2000.00, currency=Currency.RUB),
            payout_balance=PaymentAmount(value=1900.00, currency=Currency.RUB),
            status=DealStatus.CLOSED,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
            test=True,
        )

        deals_list = DealsList(items=[deal1, deal2], next_cursor="next_cursor_123")
        assert len(deals_list.list) == 2
        assert deals_list.list[0].id == "deal_123456789"
        assert deals_list.list[1].id == "deal_987654321"
        assert deals_list.next_cursor == "next_cursor_123"

    def test_deals_list_with_alias(self):
        """Test DealsList with alias 'items'."""
        deal = Deal(
            id="deal_123456789",
            fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
            balance=PaymentAmount(value=1000.00, currency=Currency.RUB),
            payout_balance=PaymentAmount(value=950.00, currency=Currency.RUB),
            status=DealStatus.OPENED,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
            test=True,
        )

        # Test with alias 'items'
        deals_list = DealsList(items=[deal])
        assert len(deals_list.list) == 1
        assert deals_list.list[0].id == "deal_123456789"

    def test_deals_list_without_cursor(self):
        """Test DealsList without next_cursor."""
        deal = Deal(
            id="deal_123456789",
            fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
            balance=PaymentAmount(value=1000.00, currency=Currency.RUB),
            payout_balance=PaymentAmount(value=950.00, currency=Currency.RUB),
            status=DealStatus.OPENED,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=90),
            test=True,
        )

        deals_list = DealsList(items=[deal])
        assert deals_list.next_cursor is None
