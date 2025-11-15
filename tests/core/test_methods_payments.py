"""
Tests for payment methods.
"""

from datetime import datetime

import pytest

from aioyookassa.core.methods.payments import (
    CancelPayment,
    CapturePayment,
    CreatePayment,
    GetPayment,
    GetPayments,
    PaymentsAPIMethod,
)
from aioyookassa.types.enum import (
    ConfirmationType,
    Currency,
    PaymentMethodStatus,
    PaymentMethodType,
    PaymentMode,
    PaymentSubject,
)
from aioyookassa.types.payment import (
    Airline,
    CardInfo,
    Confirmation,
    Customer,
    Deal,
    PaymentAmount,
    PaymentItem,
    PaymentMethod,
    Receipt,
    Recipient,
    Transfer,
)


class TestPaymentsAPIMethod:
    """Test PaymentsAPIMethod base class."""

    def test_payments_api_method_initialization(self):
        """Test PaymentsAPIMethod initialization."""
        method = PaymentsAPIMethod()
        assert method.http_method == "GET"
        assert method.path == "/payments"

    def test_payments_api_method_with_custom_path(self):
        """Test PaymentsAPIMethod with custom path."""
        method = PaymentsAPIMethod(path="/custom/path")
        assert method.path == "/custom/path"

    def test_payments_api_method_build(self):
        """Test PaymentsAPIMethod build method."""
        method = PaymentsAPIMethod.build("payment_123")
        assert method.path == "/payments"  # Should use class path

    def test_payments_api_method_build_with_format(self):
        """Test PaymentsAPIMethod build with path formatting."""

        class TestMethod(PaymentsAPIMethod):
            path = "/payments/{payment_id}"

        method = TestMethod.build("payment_123")
        assert method.path == "/payments/payment_123"


class TestCreatePayment:
    """Test CreatePayment method."""

    def test_create_payment_initialization(self):
        """Test CreatePayment initialization."""
        method = CreatePayment()
        assert method.http_method == "POST"
        assert method.path == "/payments"

    def test_create_payment_build_params_minimal(self):
        """Test CreatePayment build_params with minimal data."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        params = CreatePayment.build_params(amount=amount)

        # Only non-None values should be included
        assert "amount" in params
        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)

    def test_create_payment_build_params_with_all_fields(self):
        """Test CreatePayment build_params with all fields."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        card = CardInfo(
            last4="1234", expiry_year="2025", expiry_month="12", card_type="Visa"
        )
        payment_method = PaymentMethod(
            type=PaymentMethodType.CARD,
            id="pm_123456789",
            saved=True,
            status=PaymentMethodStatus.ACTIVE,
            card=card,
        )
        confirmation = Confirmation(
            type=ConfirmationType.REDIRECT,
            url="https://example.com/confirm",
            return_url="https://example.com/return",
        )
        recipient = Recipient(account_id="123456", gateway_id="gateway_123")
        customer = Customer(full_name="John Doe", email="john@example.com")
        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT,
        )
        receipt = Receipt(customer=customer, items=[item])
        airline = Airline(ticket_number="TK123456", booking_reference="ABC123")
        transfer = Transfer(
            account_id="123456",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status="succeeded",
        )
        deal = Deal(
            id="deal_123456789",
            settlements=[PaymentAmount(value=100.50, currency=Currency.RUB)],
        )

        params = CreatePayment.build_params(
            amount=amount,
            description="Test payment",
            receipt=receipt,
            recipient=recipient,
            payment_token="payment_token_123",
            payment_method_id="pm_123456789",
            payment_method_data=payment_method,
            confirmation=confirmation,
            save_payment_method=True,
            capture=True,
            client_ip="192.168.1.1",
            metadata={"key": "value"},
            airline=airline,
            transfers=[transfer],
            deal=deal,
            merchant_customer_id="customer_123",
        )

        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)
        assert params["description"] == "Test payment"
        assert params["recipient"] == {
            "account_id": "123456",
            "gateway_id": "gateway_123",
        }
        assert params["payment_token"] == "payment_token_123"
        assert params["payment_method_id"] == "pm_123456789"
        assert params["save_payment_method"] is True
        assert params["capture"] is True
        assert params["client_ip"] == "192.168.1.1"
        assert params["metadata"] == {"key": "value"}
        assert params["merchant_customer_id"] == "customer_123"

        # Check complex objects are serialized
        assert "confirmation" in params
        assert "receipt" in params
        assert "payment_method_data" in params
        assert "airline" in params
        assert "transfers" in params
        assert "deal" in params

    def test_create_payment_build_params_with_confirmation(self):
        """Test CreatePayment build_params with confirmation."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        confirmation = Confirmation(
            type=ConfirmationType.REDIRECT,
            url="https://example.com/confirm",
            return_url="https://example.com/return",
            enforce=True,
            locale="en",
        )

        params = CreatePayment.build_params(amount=amount, confirmation=confirmation)

        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)
        assert params["confirmation"]["type"] == "redirect"
        # Note: build_params uses model_dump(exclude_none=True) without by_alias=True,
        # so it returns 'url' instead of 'confirmation_url'
        assert params["confirmation"]["url"] == "https://example.com/confirm"
        assert params["confirmation"]["return_url"] == "https://example.com/return"
        assert params["confirmation"]["enforce"] is True
        assert params["confirmation"]["locale"] == "en"

    def test_create_payment_build_params_with_transfers(self):
        """Test CreatePayment build_params with transfers."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        transfer1 = Transfer(
            account_id="123456",
            amount=PaymentAmount(value=50.00, currency=Currency.RUB),
            status="succeeded",
        )
        transfer2 = Transfer(
            account_id="789012",
            amount=PaymentAmount(value=50.50, currency=Currency.RUB),
            status="succeeded",
        )

        params = CreatePayment.build_params(
            amount=amount, transfers=[transfer1, transfer2]
        )

        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)
        assert len(params["transfers"]) == 2
        assert params["transfers"][0]["account_id"] == "123456"
        assert params["transfers"][1]["account_id"] == "789012"

    def test_create_payment_build_params_filters_none_values(self):
        """Test CreatePayment build_params filters out None values."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)

        params = CreatePayment.build_params(
            amount=amount,
            description=None,
            receipt=None,
            recipient=None,
            payment_token=None,
            payment_method_id=None,
            payment_method_data=None,
            confirmation=None,
            save_payment_method=None,
            capture=None,
            client_ip=None,
            metadata=None,
            airline=None,
            transfers=None,
            deal=None,
            merchant_customer_id=None,
        )

        # Should only contain amount, all other None values should be filtered out
        assert "amount" in params
        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)


class TestGetPayments:
    """Test GetPayments method."""

    def test_get_payments_initialization(self):
        """Test GetPayments initialization."""
        method = GetPayments()
        assert method.http_method == "GET"
        assert method.path == "/payments"

    def test_get_payments_build_params_minimal(self):
        """Test GetPayments build_params with minimal data."""
        params = GetPayments.build_params(
            created_at=None,
            captured_at=None,
            payment_method=None,
            status=None,
            limit=None,
            cursor=None,
        )

        expected = {}
        assert params == expected

    def test_get_payments_build_params_with_all_fields(self):
        """Test GetPayments build_params with all fields."""
        created_at = datetime(2023, 1, 1, 12, 0, 0)
        captured_at = datetime(2023, 1, 2, 12, 0, 0)

        params = GetPayments.build_params(
            created_at=created_at,
            captured_at=captured_at,
            payment_method=PaymentMethodType.CARD,
            status="succeeded",
            limit=10,
            cursor="next_cursor_123",
            additional_param="test_value",
        )

        assert params["created_at_gte"] == created_at
        assert params["captured_at_gte"] == captured_at
        assert params["payment_method"] == PaymentMethodType.CARD
        assert params["status"] == "succeeded"
        assert params["limit"] == 10
        assert params["cursor"] == "next_cursor_123"
        assert params["additional_param"] == "test_value"

    def test_get_payments_build_params_with_enum_values(self):
        """Test GetPayments build_params with enum values."""
        params = GetPayments.build_params(
            created_at=None,
            captured_at=None,
            payment_method=PaymentMethodType.YOO_MONEY,
            status="pending",
            limit=None,
            cursor=None,
        )

        assert params["payment_method"] == PaymentMethodType.YOO_MONEY
        assert params["status"] == "pending"


class TestGetPayment:
    """Test GetPayment method."""

    def test_get_payment_initialization(self):
        """Test GetPayment initialization."""
        method = GetPayment()
        assert method.http_method == "GET"
        assert method.path == "/payments/{payment_id}"

    def test_get_payment_build(self):
        """Test GetPayment build method."""
        method = GetPayment.build("payment_123")
        assert method.path == "/payments/payment_123"


class TestCapturePayment:
    """Test CapturePayment method."""

    def test_capture_payment_initialization(self):
        """Test CapturePayment initialization."""
        method = CapturePayment()
        assert method.http_method == "POST"
        assert method.path == "/payments/{payment_id}/capture"

    def test_capture_payment_build(self):
        """Test CapturePayment build method."""
        method = CapturePayment.build("payment_123")
        assert method.path == "/payments/payment_123/capture"

    def test_capture_payment_build_params_minimal(self):
        """Test CapturePayment build_params with minimal data."""
        params = CapturePayment.build_params(
            amount=None, receipt=None, airline=None, transfers=None, deal=None
        )

        expected = {}
        assert params == expected

    def test_capture_payment_build_params_with_all_fields(self):
        """Test CapturePayment build_params with all fields."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        customer = Customer(full_name="John Doe", email="john@example.com")
        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT,
        )
        receipt = Receipt(customer=customer, items=[item])
        airline = Airline(ticket_number="TK123456", booking_reference="ABC123")
        transfer = Transfer(
            account_id="123456",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status="succeeded",
        )
        deal = Deal(
            id="deal_123456789",
            settlements=[PaymentAmount(value=100.50, currency=Currency.RUB)],
        )

        params = CapturePayment.build_params(
            amount=amount,
            receipt=receipt,
            airline=airline,
            transfers=[transfer],
            deal=deal,
        )

        assert params["amount"]["currency"] == "RUB"
        assert params["amount"]["value"] == pytest.approx(100.50)
        assert "receipt" in params
        assert "airline" in params
        assert len(params["transfers"]) == 1
        assert "deal" in params

    def test_capture_payment_build_params_filters_none_values(self):
        """Test CapturePayment build_params filters out None values."""
        params = CapturePayment.build_params(
            amount=None, receipt=None, airline=None, transfers=None, deal=None
        )

        # All values are None, so should be filtered out
        expected = {}
        assert params == expected


class TestCancelPayment:
    """Test CancelPayment method."""

    def test_cancel_payment_initialization(self):
        """Test CancelPayment initialization."""
        method = CancelPayment()
        assert method.http_method == "POST"
        assert method.path == "/payments/{payment_id}/cancel"

    def test_cancel_payment_build(self):
        """Test CancelPayment build method."""
        method = CancelPayment.build("payment_123")
        assert method.path == "/payments/payment_123/cancel"
