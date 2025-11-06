"""
Tests for refund types.
"""

import datetime
from decimal import Decimal

import pytest

from aioyookassa.types.enum import (
    CancellationParty,
    CancellationReason,
    ReceiptRegistration,
)
from aioyookassa.types.payment import CancellationDetails, PaymentAmount, Settlement
from aioyookassa.types.refund import (
    ElectronicCertificateData,
    Refund,
    RefundArticle,
    RefundAuthorizationDetails,
    RefundDeal,
    RefundMethod,
    RefundsList,
    RefundSource,
)


class TestRefundCancellationDetails:
    """Test CancellationDetails model (used for refunds)."""

    def test_refund_cancellation_details_creation(self):
        """Test CancellationDetails creation for refunds."""
        details = CancellationDetails(
            party=CancellationParty.MERCHANT,
            reason=CancellationReason.CANCELED_BY_MERCHANT,
        )
        assert details.party == CancellationParty.MERCHANT
        assert details.reason == CancellationReason.CANCELED_BY_MERCHANT


class TestRefundSource:
    """Test RefundSource model."""

    def test_refund_source_creation(self):
        """Test RefundSource creation."""
        source = RefundSource(
            account_id="123456", amount=PaymentAmount(value=100.50, currency="RUB")
        )
        assert source.account_id == "123456"
        assert source.amount.value == pytest.approx(100.50)

    def test_refund_source_with_platform_fee(self):
        """Test RefundSource with platform fee."""
        source = RefundSource(
            account_id="123456",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            platform_fee_amount=PaymentAmount(value=5.00, currency="RUB"),
        )
        assert source.platform_fee_amount.value == pytest.approx(5.00)


class TestRefundSettlement:
    """Test Settlement model (used for refunds)."""

    def test_refund_settlement_creation(self):
        """Test Settlement creation for refunds."""
        settlement = Settlement(
            type="payout", amount=PaymentAmount(value=100.50, currency="RUB")
        )
        assert settlement.type == "payout"
        assert settlement.amount.value == pytest.approx(100.50)


class TestRefundDeal:
    """Test RefundDeal model."""

    def test_refund_deal_creation(self):
        """Test RefundDeal creation."""
        settlement = Settlement(
            type="payout", amount=PaymentAmount(value=100.50, currency="RUB")
        )
        deal = RefundDeal(id="deal_123456789", refund_settlements=[settlement])
        assert deal.id == "deal_123456789"
        assert len(deal.refund_settlements) == 1
        assert deal.refund_settlements[0].amount.value == pytest.approx(100.50)


class TestRefundArticle:
    """Test RefundArticle model."""

    def test_refund_article_creation(self):
        """Test RefundArticle creation."""
        article = RefundArticle(
            article_number=123456,
            payment_article_number=789012,
            tru_code="TRU123456",
            quantity=1,
        )
        assert article.article_number == 123456
        assert article.payment_article_number == 789012
        assert article.tru_code == "TRU123456"
        assert article.quantity == 1

    def test_refund_article_with_different_quantity_types(self):
        """Test RefundArticle with different quantity types."""
        # Test with int
        article_int = RefundArticle(
            article_number=123456,
            payment_article_number=789012,
            tru_code="TRU123456",
            quantity=1,
        )
        assert article_int.quantity == 1

        # Test with float
        article_float = RefundArticle(
            article_number=123456,
            payment_article_number=789012,
            tru_code="TRU123456",
            quantity=1.5,
        )
        assert article_float.quantity == pytest.approx(1.5)

        # Test with string
        article_string = RefundArticle(
            article_number=123456,
            payment_article_number=789012,
            tru_code="TRU123456",
            quantity="2.5",
        )
        assert article_string.quantity == "2.5"

        # Test with Decimal
        article_decimal = RefundArticle(
            article_number=123456,
            payment_article_number=789012,
            tru_code="TRU123456",
            quantity=Decimal("3.75"),
        )
        assert article_decimal.quantity == Decimal("3.75")


class TestElectronicCertificateData:
    """Test ElectronicCertificateData model."""

    def test_electronic_certificate_data_creation(self):
        """Test ElectronicCertificateData creation."""
        cert_data = ElectronicCertificateData(
            amount=PaymentAmount(value=100.50, currency="RUB"),
            basket_id="basket_123456789",
        )
        assert cert_data.amount.value == pytest.approx(100.50)
        assert cert_data.basket_id == "basket_123456789"


class TestRefundMethod:
    """Test RefundMethod model."""

    def test_refund_method_creation(self):
        """Test RefundMethod creation."""
        method = RefundMethod(type="bank_card")
        assert method.type == "bank_card"

    def test_refund_method_with_sbp_operation_id(self):
        """Test RefundMethod with SBP operation ID."""
        method = RefundMethod(type="sbp", sbp_operation_id="sbp_123456789")
        assert method.type == "sbp"
        assert method.sbp_operation_id == "sbp_123456789"

    def test_refund_method_with_articles(self):
        """Test RefundMethod with articles."""
        article = RefundArticle(
            article_number=123456,
            payment_article_number=789012,
            tru_code="TRU123456",
            quantity=1,
        )
        method = RefundMethod(type="electronic_certificate", articles=[article])
        assert method.type == "electronic_certificate"
        assert len(method.articles) == 1
        assert method.articles[0].article_number == 123456

    def test_refund_method_with_electronic_certificate(self):
        """Test RefundMethod with electronic certificate."""
        cert_data = ElectronicCertificateData(
            amount=PaymentAmount(value=100.50, currency="RUB"),
            basket_id="basket_123456789",
        )
        method = RefundMethod(
            type="electronic_certificate", electronic_certificate=cert_data
        )
        assert method.type == "electronic_certificate"
        assert method.electronic_certificate == cert_data


class TestRefundAuthorizationDetails:
    """Test RefundAuthorizationDetails model."""

    def test_refund_authorization_details_creation(self):
        """Test RefundAuthorizationDetails creation."""
        auth_details = RefundAuthorizationDetails(rrn="123456789012")
        assert auth_details.rrn == "123456789012"

    def test_refund_authorization_details_empty(self):
        """Test RefundAuthorizationDetails with no fields."""
        auth_details = RefundAuthorizationDetails()
        assert auth_details.rrn is None


class TestRefund:
    """Test Refund model."""

    def test_refund_creation(self):
        """Test Refund creation."""
        refund = Refund(
            id="refund_123456789",
            payment_id="payment_123456789",
            status="succeeded",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            created_at=datetime.datetime.now(),
        )
        assert refund.id == "refund_123456789"
        assert refund.payment_id == "payment_123456789"
        assert refund.status == "succeeded"
        assert refund.amount.value == pytest.approx(100.50)

    def test_refund_with_optional_fields(self):
        """Test Refund with optional fields."""
        cancellation_details = CancellationDetails(
            party=CancellationParty.MERCHANT,
            reason=CancellationReason.CANCELED_BY_MERCHANT,
        )
        source = RefundSource(
            account_id="123456", amount=PaymentAmount(value=100.50, currency="RUB")
        )
        settlement = Settlement(
            type="payout", amount=PaymentAmount(value=100.50, currency="RUB")
        )
        deal = RefundDeal(id="deal_123456789", refund_settlements=[settlement])
        method = RefundMethod(type="bank_card")
        auth_details = RefundAuthorizationDetails(rrn="123456789012")

        refund = Refund(
            id="refund_123456789",
            payment_id="payment_123456789",
            status="succeeded",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            created_at=datetime.datetime.now(),
            description="Test refund",
            cancellation_details=cancellation_details,
            receipt_registration=ReceiptRegistration.SUCCEEDED,
            sources=[source],
            deal=deal,
            refund_method=method,
            refund_authorization_details=auth_details,
        )
        assert refund.description == "Test refund"
        assert refund.cancellation_details == cancellation_details
        assert refund.receipt_registration == ReceiptRegistration.SUCCEEDED
        assert len(refund.sources) == 1
        assert refund.deal == deal
        assert refund.refund_method == method
        assert refund.refund_authorization_details == auth_details


class TestRefundsList:
    """Test RefundsList model."""

    def test_refunds_list_creation(self):
        """Test RefundsList creation."""
        refund = Refund(
            id="refund_123456789",
            payment_id="payment_123456789",
            status="succeeded",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            created_at=datetime.datetime.now(),
        )
        refunds_list = RefundsList(items=[refund], next_cursor="next_cursor_123")
        assert len(refunds_list.list) == 1
        assert refunds_list.next_cursor == "next_cursor_123"

    def test_refunds_list_with_alias(self):
        """Test RefundsList with alias field."""
        refund_data = {
            "id": "refund_123456789",
            "payment_id": "payment_123456789",
            "status": "succeeded",
            "amount": {"value": "100.50", "currency": "RUB"},
            "created_at": "2023-01-01T00:00:00.000Z",
        }
        refunds_data = {"items": [refund_data], "next_cursor": "next_cursor_123"}
        refunds_list = RefundsList(**refunds_data)
        assert len(refunds_list.list) == 1
        assert refunds_list.next_cursor == "next_cursor_123"
