"""
Tests for payment types.
"""

import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from aioyookassa.types.enum import (
    CancellationParty,
    CancellationReason,
    ConfirmationType,
    Currency,
    PaymentMethodStatus,
    PaymentMethodType,
    PaymentMode,
    PaymentStatus,
    PaymentSubject,
)
from aioyookassa.types.payment import (
    Airline,
    AuthorizationDetails,
    CancellationDetails,
    CardInfo,
    Confirmation,
    Customer,
    Deal,
    Flight,
    IndustryDetails,
    MarkCodeInfo,
    MarkQuantity,
    OperationDetails,
    Passenger,
    Payment,
    PaymentAmount,
    PaymentItem,
    PaymentMethod,
    PaymentsList,
    Receipt,
    Recipient,
    Settlement,
    ThreeDSInfo,
    Transfer,
)


class TestPaymentAmount:
    """Test PaymentAmount model."""

    def test_payment_amount_with_int(self):
        """Test PaymentAmount with integer value."""
        amount = PaymentAmount(value=100, currency=Currency.RUB)
        assert amount.value == 100
        assert amount.currency == Currency.RUB

    def test_payment_amount_with_float(self):
        """Test PaymentAmount with float value."""
        amount = PaymentAmount(value=100.50, currency=Currency.USD)
        assert amount.value == pytest.approx(100.50)
        assert amount.currency == Currency.USD

    def test_payment_amount_with_string(self):
        """Test PaymentAmount with string value."""
        amount = PaymentAmount(value="100.00", currency=Currency.EUR)
        assert amount.value == "100.00"
        assert amount.currency == Currency.EUR

    def test_payment_amount_with_decimal(self):
        """Test PaymentAmount with Decimal value."""
        amount = PaymentAmount(value=Decimal("100.00"), currency=Currency.RUB)
        assert amount.value == Decimal("100.00")
        assert amount.currency == Currency.RUB

    def test_payment_amount_default_currency(self):
        """Test PaymentAmount with default currency."""
        amount = PaymentAmount(value=100)
        assert amount.value == 100
        assert amount.currency == Currency.RUB

    def test_payment_amount_with_string_currency(self):
        """Test PaymentAmount with string currency."""
        amount = PaymentAmount(value=100, currency="USD")
        assert amount.value == 100
        assert amount.currency == "USD"


class TestCardInfo:
    """Test CardInfo model."""

    def test_card_info_required_fields(self):
        """Test CardInfo with required fields."""
        card = CardInfo(
            last4="1234", expiry_year="2025", expiry_month="12", card_type="Visa"
        )
        assert card.last_four == "1234"
        assert card.expiry_year == "2025"
        assert card.expiry_month == "12"
        assert card.card_type == "Visa"

    def test_card_info_with_optional_fields(self):
        """Test CardInfo with optional fields."""
        card = CardInfo(
            last4="1234",
            expiry_year="2025",
            expiry_month="12",
            card_type="Visa",
            first6="123456",
            issuer_country="US",
            issuer_name="Test Bank",
            source="test",
        )
        assert card.first_six == "123456"
        assert card.card_country == "US"
        assert card.bank_name == "Test Bank"
        assert card.source == "test"

    def test_card_info_alias_fields(self):
        """Test CardInfo with alias fields."""
        card_data = {
            "last4": "1234",
            "expiry_year": "2025",
            "expiry_month": "12",
            "card_type": "Visa",
            "first6": "123456",
            "issuer_country": "US",
            "issuer_name": "Test Bank",
        }
        card = CardInfo(**card_data)
        assert card.last_four == "1234"
        assert card.first_six == "123456"
        assert card.card_country == "US"
        assert card.bank_name == "Test Bank"


class TestConfirmation:
    """Test Confirmation model."""

    def test_confirmation_required_fields(self):
        """Test Confirmation with required fields."""
        confirmation = Confirmation(
            type=ConfirmationType.REDIRECT, url="https://example.com/confirm"
        )
        assert confirmation.type == ConfirmationType.REDIRECT
        assert confirmation.url == "https://example.com/confirm"

    def test_confirmation_with_optional_fields(self):
        """Test Confirmation with optional fields."""
        confirmation = Confirmation(
            type=ConfirmationType.REDIRECT,
            url="https://example.com/confirm",
            enforce=True,
            locale="en",
            return_url="https://example.com/return",
        )
        assert confirmation.type == ConfirmationType.REDIRECT
        assert confirmation.url == "https://example.com/confirm"
        assert confirmation.enforce is True
        assert confirmation.locale == "en"
        assert confirmation.return_url == "https://example.com/return"

    def test_confirmation_with_url_alias(self):
        """Test Confirmation with url alias."""
        confirmation_data = {
            "type": "redirect",
            "confirmation_url": "https://example.com/confirm",
        }
        confirmation = Confirmation(**confirmation_data)
        assert confirmation.url == "https://example.com/confirm"

    def test_confirmation_embedded_requires_token(self):
        """Test that embedded type requires confirmation_token."""
        with pytest.raises(ValueError, match="confirmation_token is required"):
            Confirmation(type=ConfirmationType.EMBEDDED)

        confirmation = Confirmation(
            type=ConfirmationType.EMBEDDED, confirmation_token="token_123"
        )
        assert confirmation.confirmation_token == "token_123"

    def test_confirmation_mobile_application_requires_url(self):
        """Test that mobile_application type requires confirmation_url."""
        with pytest.raises(ValueError, match="confirmation_url is required"):
            Confirmation(type=ConfirmationType.MOBILE_APPLICATION)

        confirmation = Confirmation(
            type=ConfirmationType.MOBILE_APPLICATION,
            url="myapp://payment/confirm",
        )
        assert confirmation.url == "myapp://payment/confirm"

    def test_confirmation_qr_requires_data(self):
        """Test that qr type requires confirmation_data."""
        with pytest.raises(ValueError, match="confirmation_data is required"):
            Confirmation(type=ConfirmationType.QR_CODE)

        confirmation = Confirmation(
            type=ConfirmationType.QR_CODE, confirmation_data="QR_DATA_123"
        )
        assert confirmation.confirmation_data == "QR_DATA_123"

    def test_confirmation_redirect_requires_url(self):
        """Test that redirect type requires confirmation_url."""
        with pytest.raises(ValueError, match="confirmation_url is required"):
            Confirmation(type=ConfirmationType.REDIRECT)

    def test_confirmation_external_no_requirements(self):
        """Test that external type has no additional requirements."""
        confirmation = Confirmation(type=ConfirmationType.EXTERNAL)
        assert confirmation.type == ConfirmationType.EXTERNAL


class TestRecipient:
    """Test Recipient model."""

    def test_recipient_creation(self):
        """Test Recipient creation."""
        recipient = Recipient(account_id="123456", gateway_id="gateway_123")
        assert recipient.account_id == "123456"
        assert recipient.gateway_id == "gateway_123"


class TestCustomer:
    """Test Customer model."""

    def test_customer_with_all_fields(self):
        """Test Customer with all fields."""
        customer = Customer(
            full_name="John Doe",
            inn="1234567890",
            email="john@example.com",
            phone="+1234567890",
        )
        assert customer.full_name == "John Doe"
        assert customer.inn == "1234567890"
        assert customer.email == "john@example.com"
        assert customer.phone == "+1234567890"

    def test_customer_with_minimal_fields(self):
        """Test Customer with minimal fields."""
        customer = Customer()
        assert customer.full_name is None
        assert customer.inn is None
        assert customer.email is None
        assert customer.phone is None


class TestPaymentMethod:
    """Test PaymentMethod model."""

    def test_payment_method_required_fields(self):
        """Test PaymentMethod with required fields."""
        payment_method = PaymentMethod(
            type="bank_card",
            id="pm_123456789",
            saved=True,
            status=PaymentMethodStatus.ACTIVE,
        )
        assert payment_method.type == "bank_card"
        assert payment_method.id == "pm_123456789"
        assert payment_method.saved is True
        assert payment_method.status == PaymentMethodStatus.ACTIVE

    def test_payment_method_with_card(self):
        """Test PaymentMethod with card info."""
        card = CardInfo(
            last4="1234", expiry_year="2025", expiry_month="12", card_type="Visa"
        )
        payment_method = PaymentMethod(
            type="bank_card",
            id="pm_123456789",
            saved=True,
            status=PaymentMethodStatus.ACTIVE,
            card=card,
        )
        assert payment_method.card == card


class TestCancellationDetails:
    """Test CancellationDetails model."""

    def test_cancellation_details_creation(self):
        """Test CancellationDetails creation."""
        details = CancellationDetails(
            party=CancellationParty.MERCHANT,
            reason=CancellationReason.CANCELED_BY_MERCHANT,
        )
        assert details.party == CancellationParty.MERCHANT
        assert details.reason == CancellationReason.CANCELED_BY_MERCHANT


class TestThreeDSInfo:
    """Test ThreeDSInfo model."""

    def test_three_ds_info_creation(self):
        """Test ThreeDSInfo creation."""
        three_ds = ThreeDSInfo(applied=True)
        assert three_ds.applied is True


class TestAuthorizationDetails:
    """Test AuthorizationDetails model."""

    def test_authorization_details_creation(self):
        """Test AuthorizationDetails creation."""
        auth_details = AuthorizationDetails(
            rrn="123456789",
            auth_code="AUTH123",
            three_d_secure=ThreeDSInfo(applied=True),
        )
        assert auth_details.transaction_identifier == "123456789"
        assert auth_details.authorization_code == "AUTH123"
        assert auth_details.three_d_secure.applied is True

    def test_authorization_details_with_alias(self):
        """Test AuthorizationDetails with alias fields."""
        auth_data = {
            "rrn": "123456789",
            "auth_code": "AUTH123",
            "three_d_secure": {"applied": True},
        }
        auth_details = AuthorizationDetails(**auth_data)
        assert auth_details.transaction_identifier == "123456789"
        assert auth_details.authorization_code == "AUTH123"


class TestTransfer:
    """Test Transfer model."""

    def test_transfer_creation(self):
        """Test Transfer creation."""
        transfer = Transfer(
            account_id="123456",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PaymentStatus.SUCCEEDED,
        )
        assert transfer.account_id == "123456"
        assert transfer.amount.value == pytest.approx(100.50)
        assert transfer.status == PaymentStatus.SUCCEEDED

    def test_transfer_with_optional_fields(self):
        """Test Transfer with optional fields."""
        transfer = Transfer(
            account_id="123456",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            status=PaymentStatus.SUCCEEDED,
            platform_fee_amount=PaymentAmount(value=5.00, currency=Currency.RUB),
            description="Test transfer",
            metadata={"key": "value"},
        )
        assert transfer.fee_amount.value == 5.00
        assert transfer.description == "Test transfer"
        assert transfer.metadata == {"key": "value"}

    def test_transfer_with_fee_amount_alias(self):
        """Test Transfer with fee_amount alias."""
        transfer_data = {
            "account_id": "123456",
            "amount": {"value": "100.50", "currency": "RUB"},
            "status": "succeeded",
            "platform_fee_amount": {"value": "5.00", "currency": "RUB"},
        }
        transfer = Transfer(**transfer_data)
        assert transfer.fee_amount.value == "5.00"


class TestSettlement:
    """Test Settlement model."""

    def test_settlement_creation(self):
        """Test Settlement creation."""
        settlement = Settlement(
            type="payout", amount=PaymentAmount(value=100.50, currency=Currency.RUB)
        )
        assert settlement.type == "payout"
        assert settlement.amount.value == pytest.approx(100.50)


class TestDeal:
    """Test Deal model."""

    def test_deal_creation(self):
        """Test Deal creation."""
        deal = Deal(
            id="deal_123456789",
            settlements=[PaymentAmount(value=100.50, currency=Currency.RUB)],
        )
        assert deal.id == "deal_123456789"
        assert len(deal.settlements) == 1
        assert deal.settlements[0].value == pytest.approx(100.50)


class TestMarkQuantity:
    """Test MarkQuantity model."""

    def test_mark_quantity_creation(self):
        """Test MarkQuantity creation."""
        mark_quantity = MarkQuantity(numerator=1, denominator=2)
        assert mark_quantity.numerator == 1
        assert mark_quantity.denominator == 2


class TestMarkCodeInfo:
    """Test MarkCodeInfo model."""

    def test_mark_code_info_creation(self):
        """Test MarkCodeInfo creation."""
        mark_code = MarkCodeInfo(
            mark_code_raw="12345678901234567890",
            ean_13="1234567890123",
            gs_10="1234567890",
        )
        assert mark_code.code == "12345678901234567890"
        assert mark_code.ean_13 == "1234567890123"
        assert mark_code.gs_10 == "1234567890"

    def test_mark_code_info_with_alias(self):
        """Test MarkCodeInfo with alias field."""
        mark_code_data = {
            "mark_code_raw": "12345678901234567890",
            "ean_13": "1234567890123",
        }
        mark_code = MarkCodeInfo(**mark_code_data)
        assert mark_code.code == "12345678901234567890"


class TestIndustryDetails:
    """Test IndustryDetails model."""

    def test_industry_details_creation(self):
        """Test IndustryDetails creation."""
        industry = IndustryDetails(
            federal_id="1234567890",
            document_date=datetime.datetime.now(),
            document_number="DOC123",
            value="Test value",
        )
        assert industry.federal_id == "1234567890"
        assert industry.document_number == "DOC123"
        assert industry.value == "Test value"


class TestOperationDetails:
    """Test OperationDetails model."""

    def test_operation_details_creation(self):
        """Test OperationDetails creation."""
        operation = OperationDetails(
            operation_id=123456, value="Test value", created_at=datetime.datetime.now()
        )
        assert operation.id == 123456
        assert operation.value == "Test value"

    def test_operation_details_with_alias(self):
        """Test OperationDetails with alias field."""
        operation_data = {
            "operation_id": 123456,
            "value": "Test value",
            "created_at": "2023-01-01T00:00:00.000Z",
        }
        operation = OperationDetails(**operation_data)
        assert operation.id == 123456


class TestPassenger:
    """Test Passenger model."""

    def test_passenger_creation(self):
        """Test Passenger creation."""
        passenger = Passenger(first_name="John", last_name="Doe")
        assert passenger.first_name == "John"
        assert passenger.last_name == "Doe"


class TestFlight:
    """Test Flight model."""

    def test_flight_creation(self):
        """Test Flight creation."""
        flight = Flight(
            departure_airport="SVO",
            arrival_airport="LED",
            departure_date=datetime.datetime.now(),
        )
        assert flight.departure_airport == "SVO"
        assert flight.arrival_airport == "LED"

    def test_flight_with_optional_fields(self):
        """Test Flight with optional fields."""
        flight = Flight(
            departure_airport="SVO",
            arrival_airport="LED",
            departure_date=datetime.datetime.now(),
            carrier_code="SU",
        )
        assert flight.carrier_code == "SU"


class TestAirline:
    """Test Airline model."""

    def test_airline_creation(self):
        """Test Airline creation."""
        airline = Airline(ticket_number="TK123456", booking_reference="ABC123")
        assert airline.ticket_number == "TK123456"
        assert airline.booking_reference == "ABC123"

    def test_airline_with_passengers_and_flights(self):
        """Test Airline with passengers and flights."""
        passenger = Passenger(first_name="John", last_name="Doe")
        flight = Flight(
            departure_airport="SVO",
            arrival_airport="LED",
            departure_date=datetime.datetime.now(),
        )
        airline = Airline(
            ticket_number="TK123456", passengers=[passenger], legs=[flight]
        )
        assert len(airline.passengers) == 1
        assert len(airline.flights) == 1

    def test_airline_with_flights_alias(self):
        """Test Airline with flights alias."""
        flight_data = {
            "departure_airport": "SVO",
            "arrival_airport": "LED",
            "departure_date": "2023-01-01T00:00:00.000Z",
        }
        airline_data = {"ticket_number": "TK123456", "legs": [flight_data]}
        airline = Airline(**airline_data)
        assert len(airline.flights) == 1
        assert airline.flights[0].departure_airport == "SVO"


class TestPaymentItem:
    """Test PaymentItem model."""

    def test_payment_item_creation(self):
        """Test PaymentItem creation."""
        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT,
        )
        assert item.description == "Test item"
        assert item.amount.value == pytest.approx(100.50)
        assert item.vat_code == 1
        assert item.quantity == 1
        assert item.payment_subject == PaymentSubject.COMMODITY
        assert item.payment_mode == PaymentMode.FULL_PAYMENT

    def test_payment_item_with_optional_fields(self):
        """Test PaymentItem with optional fields."""
        mark_quantity = MarkQuantity(numerator=1, denominator=2)
        mark_code = MarkCodeInfo(code="12345678901234567890")
        industry = IndustryDetails(
            federal_id="1234567890",
            document_date=datetime.datetime.now(),
            document_number="DOC123",
            value="Test value",
        )

        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT,
            measure="piece",
            mark_quantity=mark_quantity,
            country_of_origin_code="RU",
            customs_declaration_number="1234567890",
            excise="0.00",
            product_code="1234567890123",
            mark_code_info=mark_code,
            mark_mode="unknown",
            payment_subject_industry_details=industry,
        )
        assert item.measure == "piece"
        assert item.mark_quantity == mark_quantity
        assert item.country_of_origin_code == "RU"
        assert item.customs_declaration_number == "1234567890"
        assert item.excise == "0.00"
        assert item.product_code == "1234567890123"
        assert item.mark_code_info == mark_code
        assert item.mark_mode == "unknown"
        assert item.payment_subject_industry_details == industry


class TestReceipt:
    """Test Receipt model."""

    def test_receipt_creation(self):
        """Test Receipt creation."""
        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT,
        )
        receipt = Receipt(items=[item])
        assert len(receipt.items) == 1
        assert receipt.items[0].description == "Test item"

    def test_receipt_with_optional_fields(self):
        """Test Receipt with optional fields."""
        customer = Customer(full_name="John Doe", email="john@example.com")
        item = PaymentItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT,
        )
        industry = IndustryDetails(
            federal_id="1234567890",
            document_date=datetime.datetime.now(),
            document_number="DOC123",
            value="Test value",
        )
        operation = OperationDetails(
            operation_id=123456, value="Test value", created_at=datetime.datetime.now()
        )

        receipt = Receipt(
            customer=customer,
            items=[item],
            phone="+1234567890",
            email="john@example.com",
            tax_system_code=1,
            internet=True,
            timezone=3,
            receipt_industry_details=[industry],
            receipt_operation_details=operation,
        )
        assert receipt.customer == customer
        assert receipt.phone == "+1234567890"
        assert receipt.email == "john@example.com"
        assert receipt.tax_system_code == 1
        assert receipt.internet is True
        assert receipt.timezone == 3
        assert len(receipt.receipt_industry_details) == 1
        assert receipt.receipt_operation_details == operation


class TestPayment:
    """Test Payment model."""

    def test_payment_creation(self):
        """Test Payment creation."""
        payment = Payment(
            id="payment_123456789",
            status=PaymentStatus.SUCCEEDED,
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            recipient=Recipient(account_id="123456", gateway_id="gateway_123"),
            created_at=datetime.datetime.now(),
            test=True,
            paid=True,
            refundable=True,
        )
        assert payment.id == "payment_123456789"
        assert payment.status == PaymentStatus.SUCCEEDED
        assert payment.amount.value == pytest.approx(100.50)
        assert payment.test is True
        assert payment.paid is True
        assert payment.refundable is True

    def test_payment_with_optional_fields(self):
        """Test Payment with optional fields."""
        payment_method = PaymentMethod(
            type="bank_card",
            id="pm_123456789",
            saved=True,
            status=PaymentMethodStatus.ACTIVE,
        )
        confirmation = Confirmation(
            type=ConfirmationType.REDIRECT, url="https://example.com/confirm"
        )
        cancellation_details = CancellationDetails(
            party=CancellationParty.MERCHANT,
            reason=CancellationReason.CANCELED_BY_MERCHANT,
        )

        payment = Payment(
            id="payment_123456789",
            status=PaymentStatus.SUCCEEDED,
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            recipient=Recipient(account_id="123456", gateway_id="gateway_123"),
            created_at=datetime.datetime.now(),
            test=True,
            paid=True,
            refundable=True,
            income_amount=PaymentAmount(value=95.50, currency=Currency.RUB),
            description="Test payment",
            payment_method=payment_method,
            captured_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
            confirmation=confirmation,
            refunded_amount=PaymentAmount(value=50.00, currency=Currency.RUB),
            receipt_registration="succeeded",
            metadata={"key": "value"},
            cancellation_details=cancellation_details,
            merchant_customer_id="customer_123",
        )
        assert payment.income_amount.value == 95.50
        assert payment.description == "Test payment"
        assert payment.payment_method == payment_method
        assert payment.confirmation == confirmation
        assert payment.refunded_amount.value == 50.00
        assert payment.receipt_registration == "succeeded"
        assert payment.metadata == {"key": "value"}
        assert payment.cancellation_details == cancellation_details
        assert payment.merchant_customer_id == "customer_123"


class TestPaymentsList:
    """Test PaymentsList model."""

    def test_payments_list_creation(self):
        """Test PaymentsList creation."""
        payment = Payment(
            id="payment_123456789",
            status=PaymentStatus.SUCCEEDED,
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            recipient=Recipient(account_id="123456", gateway_id="gateway_123"),
            created_at=datetime.datetime.now(),
            test=True,
            paid=True,
            refundable=True,
        )
        payments_list = PaymentsList(items=[payment], cursor="next_cursor_123")
        assert len(payments_list.list) == 1
        assert payments_list.cursor == "next_cursor_123"

    def test_payments_list_with_alias(self):
        """Test PaymentsList with alias field."""
        payment_data = {
            "id": "payment_123456789",
            "status": "succeeded",
            "amount": {"value": "100.50", "currency": "RUB"},
            "recipient": {"account_id": "123456", "gateway_id": "gateway_123"},
            "created_at": "2023-01-01T00:00:00.000Z",
            "test": True,
            "paid": True,
            "refundable": True,
        }
        payments_data = {"items": [payment_data], "cursor": "next_cursor_123"}
        payments_list = PaymentsList(**payments_data)
        assert len(payments_list.list) == 1
        assert payments_list.cursor == "next_cursor_123"
