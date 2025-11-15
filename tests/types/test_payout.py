"""
Tests for payout types.
"""

import datetime

import pytest

from aioyookassa.types.enum import (
    CancellationParty,
    CancellationReason,
    Currency,
    PayoutStatus,
)
from aioyookassa.types.payment import CancellationDetails, Deal, PaymentAmount
from aioyookassa.types.payout import (
    BankCardPayoutDestination,
    Payout,
    PayoutCardInfo,
    PayoutReceipt,
    SbpPayoutDestination,
    SelfEmployed,
    YooMoneyPayoutDestination,
)


class TestPayoutCardInfo:
    """Test PayoutCardInfo model."""

    def test_payout_card_info_creation(self):
        """Test PayoutCardInfo creation."""
        card_info = PayoutCardInfo(
            first6="123456",
            last4="7890",
            card_type="Visa",
            issuer_country="RU",
            issuer_name="Test Bank",
        )
        assert card_info.first6 == "123456"
        assert card_info.last4 == "7890"
        assert card_info.card_type == "Visa"
        assert card_info.issuer_country == "RU"
        assert card_info.issuer_name == "Test Bank"

    def test_payout_card_info_minimal(self):
        """Test PayoutCardInfo with minimal fields."""
        card_info = PayoutCardInfo(
            first6="123456", last4="7890", card_type="MasterCard"
        )
        assert card_info.first6 == "123456"
        assert card_info.last4 == "7890"
        assert card_info.card_type == "MasterCard"
        assert card_info.issuer_country is None
        assert card_info.issuer_name is None


class TestBankCardPayoutDestination:
    """Test BankCardPayoutDestination model."""

    def test_bank_card_payout_destination_creation(self):
        """Test BankCardPayoutDestination creation."""
        card_info = PayoutCardInfo(first6="123456", last4="7890", card_type="Visa")
        destination = BankCardPayoutDestination(card=card_info)
        assert destination.type == "bank_card"
        assert destination.card == card_info


class TestSbpPayoutDestination:
    """Test SbpPayoutDestination model."""

    def test_sbp_payout_destination_creation(self):
        """Test SbpPayoutDestination creation."""
        destination = SbpPayoutDestination(
            bank_id="100000000001", phone="79000000000", recipient_checked=True
        )
        assert destination.type == "sbp"
        assert destination.bank_id == "100000000001"
        assert destination.phone == "79000000000"
        assert destination.recipient_checked is True

    def test_sbp_payout_destination_without_check(self):
        """Test SbpPayoutDestination without recipient check."""
        destination = SbpPayoutDestination(
            bank_id="100000000001", phone="79000000000", recipient_checked=False
        )
        assert destination.recipient_checked is False


class TestYooMoneyPayoutDestination:
    """Test YooMoneyPayoutDestination model."""

    def test_yoo_money_payout_destination_creation(self):
        """Test YooMoneyPayoutDestination creation."""
        destination = YooMoneyPayoutDestination(account_number="41001614575714")
        assert destination.type == "yoo_money"
        assert destination.account_number == "41001614575714"


class TestPayoutReceipt:
    """Test PayoutReceipt model."""

    def test_payout_receipt_creation(self):
        """Test PayoutReceipt creation."""
        receipt = PayoutReceipt(
            service_name="Test service",
            npd_receipt_id="208jd98zqe",
            url="https://www.nalog.gov.ru/api/v1/receipt/208jd98zqe/print",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        )
        assert receipt.service_name == "Test service"
        assert receipt.npd_receipt_id == "208jd98zqe"
        assert receipt.url == "https://www.nalog.gov.ru/api/v1/receipt/208jd98zqe/print"
        assert receipt.amount.value == pytest.approx(100.50)

    def test_payout_receipt_minimal(self):
        """Test PayoutReceipt with minimal fields."""
        receipt = PayoutReceipt(service_name="Test service")
        assert receipt.service_name == "Test service"
        assert receipt.npd_receipt_id is None
        assert receipt.url is None
        assert receipt.amount is None


class TestPayoutDeal:
    """Test Deal model used in Payout."""

    def test_payout_deal_creation(self):
        """Test Deal creation for payout."""
        deal = Deal(id="deal_123456789")
        assert deal.id == "deal_123456789"
        assert deal.settlements is None


class TestSelfEmployed:
    """Test SelfEmployed model."""

    def test_self_employed_creation(self):
        """Test SelfEmployed creation."""
        self_employed = SelfEmployed(id="se_123456789")
        assert self_employed.id == "se_123456789"


class TestPayoutCancellationDetails:
    """Test CancellationDetails model used in Payout."""

    def test_payout_cancellation_details_creation(self):
        """Test CancellationDetails creation for payout."""
        details = CancellationDetails(
            party=CancellationParty.MERCHANT,
            reason=CancellationReason.CANCELED_BY_MERCHANT,
        )
        assert details.party == CancellationParty.MERCHANT
        assert details.reason == CancellationReason.CANCELED_BY_MERCHANT


class TestPayout:
    """Test Payout model."""

    def test_payout_creation_minimal(self):
        """Test Payout creation with minimal fields."""
        card_info = PayoutCardInfo(first6="123456", last4="7890", card_type="Visa")
        destination = BankCardPayoutDestination(card=card_info)

        payout = Payout(
            id="payout_123456789",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PayoutStatus.PENDING,
            payout_destination=destination,
            created_at=datetime.datetime.now(),
            test=True,
        )
        assert payout.id == "payout_123456789"
        assert payout.amount.value == pytest.approx(100.50)
        assert payout.status == PayoutStatus.PENDING
        assert payout.payout_destination == destination
        assert payout.test is True

    def test_payout_with_all_fields(self):
        """Test Payout with all fields."""
        card_info = PayoutCardInfo(
            first6="123456",
            last4="7890",
            card_type="Visa",
            issuer_country="RU",
            issuer_name="Test Bank",
        )
        destination = BankCardPayoutDestination(card=card_info)
        deal = Deal(id="deal_123456789")
        self_employed = SelfEmployed(id="se_123456789")
        receipt = PayoutReceipt(
            service_name="Test service",
            npd_receipt_id="208jd98zqe",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        )
        cancellation_details = CancellationDetails(
            party=CancellationParty.MERCHANT,
            reason=CancellationReason.CANCELED_BY_MERCHANT,
        )

        payout = Payout(
            id="payout_123456789",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PayoutStatus.SUCCEEDED,
            payout_destination=destination,
            description="Test payout",
            created_at=datetime.datetime.now(),
            succeeded_at=datetime.datetime.now(),
            deal=deal,
            self_employed=self_employed,
            receipt=receipt,
            cancellation_details=cancellation_details,
            metadata={"key": "value"},
            test=False,
        )
        assert payout.description == "Test payout"
        assert payout.succeeded_at is not None
        assert payout.deal == deal
        assert payout.self_employed == self_employed
        assert payout.receipt == receipt
        assert payout.cancellation_details == cancellation_details
        assert payout.metadata == {"key": "value"}
        assert payout.test is False

    def test_payout_with_sbp_destination(self):
        """Test Payout with SBP destination."""
        destination = SbpPayoutDestination(
            bank_id="100000000001", phone="79000000000", recipient_checked=True
        )

        payout = Payout(
            id="payout_123456789",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PayoutStatus.PENDING,
            payout_destination=destination,
            created_at=datetime.datetime.now(),
            test=True,
        )
        assert isinstance(payout.payout_destination, SbpPayoutDestination)
        assert payout.payout_destination.bank_id == "100000000001"

    def test_payout_with_yoo_money_destination(self):
        """Test Payout with YooMoney destination."""
        destination = YooMoneyPayoutDestination(account_number="41001614575714")

        payout = Payout(
            id="payout_123456789",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PayoutStatus.PENDING,
            payout_destination=destination,
            created_at=datetime.datetime.now(),
            test=True,
        )
        assert isinstance(payout.payout_destination, YooMoneyPayoutDestination)
        assert payout.payout_destination.account_number == "41001614575714"
