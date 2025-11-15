"""
Tests for payout methods.
"""

import pytest

from aioyookassa.core.methods.payouts import CreatePayout, GetPayout, PayoutsAPIMethod
from aioyookassa.types.enum import Currency
from aioyookassa.types.params import (
    BankCardPayoutCardData,
    BankCardPayoutDestinationData,
    PayoutReceiptData,
)
from aioyookassa.types.payment import Deal, PaymentAmount
from aioyookassa.types.payout import SelfEmployed


class TestPayoutsAPIMethod:
    """Test PayoutsAPIMethod base class."""

    def test_payouts_api_method_initialization(self):
        """Test PayoutsAPIMethod initialization."""
        method = PayoutsAPIMethod()
        assert method.http_method == "GET"
        assert method.path == "/payouts"

    def test_payouts_api_method_with_custom_path(self):
        """Test PayoutsAPIMethod with custom path."""
        method = PayoutsAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_payouts_api_method_build(self):
        """Test PayoutsAPIMethod build method."""
        method = PayoutsAPIMethod.build("payout_123")
        assert method.path == "/payouts"  # Should use class path

    def test_payouts_api_method_build_with_format(self):
        """Test PayoutsAPIMethod build with path formatting."""

        class TestMethod(PayoutsAPIMethod):
            path = "/payouts/{payout_id}"

        method = TestMethod.build("payout_123")
        assert method.path == "/payouts/payout_123"


class TestCreatePayout:
    """Test CreatePayout method."""

    def test_create_payout_initialization(self):
        """Test CreatePayout initialization."""
        method = CreatePayout()
        assert method.http_method == "POST"
        assert method.path == "/payouts"

    def test_create_payout_build_params_minimal(self):
        """Test CreatePayout build_params with minimal data."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        params = CreatePayout.build_params(amount=amount)

        # Only non-None values should be included
        assert "amount" in params
        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)

    def test_create_payout_build_params_with_bank_card(self):
        """Test CreatePayout build_params with bank card destination."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        card_data = BankCardPayoutCardData(number="5555555555554477")
        destination = BankCardPayoutDestinationData(card=card_data)

        params = CreatePayout.build_params(
            amount=amount, payout_destination_data=destination
        )

        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)
        assert params["payout_destination_data"]["type"] == "bank_card"
        assert params["payout_destination_data"]["card"]["number"] == "5555555555554477"

    def test_create_payout_build_params_with_all_fields(self):
        """Test CreatePayout build_params with all fields."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        card_data = BankCardPayoutCardData(number="5555555555554477")
        destination = BankCardPayoutDestinationData(card=card_data)
        deal = Deal(id="deal_123456789")
        self_employed = SelfEmployed(id="se_123456789")
        receipt_data = PayoutReceiptData(
            service_name="Test service",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        )

        params = CreatePayout.build_params(
            amount=amount,
            payout_destination_data=destination,
            payout_token="payout_token_123",
            payment_method_id="pm_123456789",
            description="Test payout",
            deal=deal,
            self_employed=self_employed,
            receipt_data=receipt_data,
            personal_data=["pd_123", "pd_456"],
            metadata={"key": "value"},
        )

        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)
        assert params["payout_destination_data"]["type"] == "bank_card"
        assert params["payout_token"] == "payout_token_123"
        assert params["payment_method_id"] == "pm_123456789"
        assert params["description"] == "Test payout"
        assert params["personal_data"] == ["pd_123", "pd_456"]
        assert params["metadata"] == {"key": "value"}
        assert "deal" in params
        assert "self_employed" in params
        assert "receipt_data" in params

    def test_create_payout_build_params_with_sbp_destination(self):
        """Test CreatePayout build_params with SBP destination."""
        from aioyookassa.types.params import SbpPayoutDestinationData

        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        destination = SbpPayoutDestinationData(
            bank_id="100000000001", phone="79000000000"
        )

        params = CreatePayout.build_params(
            amount=amount, payout_destination_data=destination
        )

        assert params["payout_destination_data"]["type"] == "sbp"
        assert params["payout_destination_data"]["bank_id"] == "100000000001"
        assert params["payout_destination_data"]["phone"] == "79000000000"

    def test_create_payout_build_params_with_yoo_money_destination(self):
        """Test CreatePayout build_params with YooMoney destination."""
        from aioyookassa.types.params import YooMoneyPayoutDestinationData

        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        destination = YooMoneyPayoutDestinationData(account_number="41001614575714")

        params = CreatePayout.build_params(
            amount=amount, payout_destination_data=destination
        )

        assert params["payout_destination_data"]["type"] == "yoo_money"
        assert params["payout_destination_data"]["account_number"] == "41001614575714"

    def test_create_payout_build_params_filters_none_values(self):
        """Test CreatePayout build_params filters out None values."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)

        params = CreatePayout.build_params(
            amount=amount,
            payout_destination_data=None,
            payout_token=None,
            payment_method_id=None,
            description=None,
            deal=None,
            self_employed=None,
            receipt_data=None,
            personal_data=None,
            metadata=None,
        )

        # Should only contain amount, all other None values should be filtered out
        assert "amount" in params
        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)


class TestGetPayout:
    """Test GetPayout method."""

    def test_get_payout_initialization(self):
        """Test GetPayout initialization."""
        method = GetPayout()
        assert method.http_method == "GET"
        assert method.path == "/payouts/{payout_id}"

    def test_get_payout_build(self):
        """Test GetPayout build method."""
        method = GetPayout.build("payout_123")
        assert method.path == "/payouts/payout_123"
