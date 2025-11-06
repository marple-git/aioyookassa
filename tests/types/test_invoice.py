"""
Tests for invoice types.
"""

import datetime
from decimal import Decimal

import pytest

from aioyookassa.types.enum import Currency
from aioyookassa.types.invoice import (
    Invoice,
    InvoiceCartItem,
    InvoiceDeliveryMethodData,
    InvoicePaymentData,
    InvoiceReceipt,
    InvoiceReceiptItem,
)
from aioyookassa.types.payment import (
    Customer,
    IndustryDetails,
    MarkCodeInfo,
    MarkQuantity,
    OperationDetails,
    PaymentAmount,
    Recipient,
)


class TestInvoiceCartItem:
    """Test InvoiceCartItem model."""

    def test_invoice_cart_item_creation(self):
        """Test InvoiceCartItem creation."""
        item = InvoiceCartItem(
            description="Test invoice item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            quantity=1,
        )
        assert item.description == "Test invoice item"
        assert item.price.value == pytest.approx(100.50)
        assert item.quantity == 1

    def test_invoice_cart_item_with_discount_price(self):
        """Test InvoiceCartItem with discount price."""
        item = InvoiceCartItem(
            description="Test invoice item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            discount_price=PaymentAmount(value=90.00, currency=Currency.RUB),
            quantity=1,
        )
        assert item.discount_price.value == 90.00

    def test_invoice_cart_item_with_different_quantity_types(self):
        """Test InvoiceCartItem with different quantity types."""
        # Test with int
        item_int = InvoiceCartItem(
            description="Test item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            quantity=1,
        )
        assert item_int.quantity == 1

        # Test with float
        item_float = InvoiceCartItem(
            description="Test item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            quantity=1.5,
        )
        assert item_float.quantity == pytest.approx(1.5)

        # Test with string
        item_string = InvoiceCartItem(
            description="Test item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            quantity="2.5",
        )
        assert item_string.quantity == "2.5"

        # Test with Decimal
        item_decimal = InvoiceCartItem(
            description="Test item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            quantity=Decimal("3.75"),
        )
        assert item_decimal.quantity == Decimal("3.75")


class TestInvoiceDeliveryMethodData:
    """Test InvoiceDeliveryMethodData model."""

    def test_invoice_delivery_method_data_creation(self):
        """Test InvoiceDeliveryMethodData creation."""
        delivery = InvoiceDeliveryMethodData(type="self")
        assert delivery.type == "self"


class TestInvoiceReceiptItem:
    """Test InvoiceReceiptItem model."""

    def test_invoice_receipt_item_creation(self):
        """Test InvoiceReceiptItem creation."""
        item = InvoiceReceiptItem(
            description="Test invoice receipt item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
        )
        assert item.description == "Test invoice receipt item"
        assert item.amount.value == pytest.approx(100.50)
        assert item.vat_code == 1
        assert item.quantity == 1

    def test_invoice_receipt_item_with_optional_fields(self):
        """Test InvoiceReceiptItem with optional fields."""
        mark_quantity = MarkQuantity(numerator=1, denominator=2)
        mark_code = MarkCodeInfo(code="12345678901234567890")
        industry = IndustryDetails(
            federal_id="1234567890",
            document_date=datetime.datetime.now(),
            document_number="DOC123",
            value="Test value",
        )

        item = InvoiceReceiptItem(
            description="Test invoice receipt item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
            measure="piece",
            mark_quantity=mark_quantity,
            payment_subject="commodity",
            payment_mode="full_payment",
            country_of_origin_code="RU",
            customs_declaration_number="1234567890",
            excise="0.00",
            product_code="1234567890123",
            planned_status=1,
            mark_code_info=mark_code,
            mark_mode="unknown",
            payment_subject_industry_details=[industry],
        )
        assert item.measure == "piece"
        assert item.mark_quantity == mark_quantity
        assert item.payment_subject == "commodity"
        assert item.payment_mode == "full_payment"
        assert item.country_of_origin_code == "RU"
        assert item.customs_declaration_number == "1234567890"
        assert item.excise == "0.00"
        assert item.product_code == "1234567890123"
        assert item.planned_status == 1
        assert item.mark_code_info == mark_code
        assert item.mark_mode == "unknown"
        assert len(item.payment_subject_industry_details) == 1

    def test_invoice_receipt_item_with_different_quantity_types(self):
        """Test InvoiceReceiptItem with different quantity types."""
        # Test with int
        item_int = InvoiceReceiptItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
        )
        assert item_int.quantity == 1

        # Test with float
        item_float = InvoiceReceiptItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1.5,
        )
        assert item_float.quantity == 1.5

        # Test with string
        item_string = InvoiceReceiptItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity="2.5",
        )
        assert item_string.quantity == "2.5"

        # Test with Decimal
        item_decimal = InvoiceReceiptItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=Decimal("3.75"),
        )
        assert item_decimal.quantity == Decimal("3.75")


class TestInvoiceReceipt:
    """Test InvoiceReceipt model."""

    def test_invoice_receipt_creation(self):
        """Test InvoiceReceipt creation."""
        item = InvoiceReceiptItem(
            description="Test invoice receipt item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
        )
        receipt = InvoiceReceipt(items=[item])
        assert len(receipt.items) == 1
        assert receipt.items[0].description == "Test invoice receipt item"

    def test_invoice_receipt_with_optional_fields(self):
        """Test InvoiceReceipt with optional fields."""
        customer = Customer(full_name="John Doe", email="john@example.com")
        item = InvoiceReceiptItem(
            description="Test invoice receipt item",
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            vat_code=1,
            quantity=1,
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

        receipt = InvoiceReceipt(
            customer=customer,
            items=[item],
            internet=True,
            tax_system_code=1,
            timezone=3,
            receipt_industry_details=[industry],
            receipt_operational_details=operation,
        )
        assert receipt.customer == customer
        assert receipt.internet is True
        assert receipt.tax_system_code == 1
        assert receipt.timezone == 3
        assert len(receipt.receipt_industry_details) == 1
        assert receipt.receipt_operational_details == operation


class TestInvoicePaymentData:
    """Test InvoicePaymentData model."""

    def test_invoice_payment_data_creation(self):
        """Test InvoicePaymentData creation."""
        payment_data = InvoicePaymentData(
            amount=PaymentAmount(value=100.50, currency=Currency.RUB)
        )
        assert payment_data.amount.value == pytest.approx(100.50)

    def test_invoice_payment_data_with_optional_fields(self):
        """Test InvoicePaymentData with optional fields."""
        receipt = InvoiceReceipt(
            items=[
                InvoiceReceiptItem(
                    description="Test item",
                    amount=PaymentAmount(value=100.50, currency=Currency.RUB),
                    vat_code=1,
                    quantity=1,
                )
            ]
        )
        recipient = Recipient(account_id="123456", gateway_id="gateway_123")

        payment_data = InvoicePaymentData(
            amount=PaymentAmount(value=100.50, currency=Currency.RUB),
            receipt=receipt,
            recipient=recipient,
            save_payment_method=True,
            capture=True,
            client_ip="192.168.1.1",
            description="Test payment",
            metadata={"key": "value"},
        )
        assert payment_data.receipt == receipt
        assert payment_data.recipient == recipient
        assert payment_data.save_payment_method is True
        assert payment_data.capture is True
        assert payment_data.client_ip == "192.168.1.1"
        assert payment_data.description == "Test payment"
        assert payment_data.metadata == {"key": "value"}


class TestInvoice:
    """Test Invoice model."""

    def test_invoice_creation(self):
        """Test Invoice creation."""
        cart_item = InvoiceCartItem(
            description="Test invoice item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            quantity=1,
        )
        invoice = Invoice(
            id="invoice_123456789",
            status="active",
            cart=[cart_item],
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
        )
        assert invoice.id == "invoice_123456789"
        assert invoice.status == "active"
        assert len(invoice.cart) == 1
        assert invoice.cart[0].description == "Test invoice item"

    def test_invoice_with_optional_fields(self):
        """Test Invoice with optional fields."""
        cart_item = InvoiceCartItem(
            description="Test invoice item",
            price=PaymentAmount(value=100.50, currency=Currency.RUB),
            quantity=1,
        )
        delivery_method = InvoiceDeliveryMethodData(type="self")
        payment_data = InvoicePaymentData(
            amount=PaymentAmount(value=100.50, currency=Currency.RUB)
        )

        invoice = Invoice(
            id="invoice_123456789",
            status="active",
            cart=[cart_item],
            delivery_method_data=delivery_method,
            payment_data=payment_data,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
            locale="en",
            description="Test invoice",
            metadata={"key": "value"},
            url="https://example.com/invoice/123456789",
        )
        assert invoice.delivery_method_data == delivery_method
        assert invoice.payment_data == payment_data
        assert invoice.locale == "en"
        assert invoice.description == "Test invoice"
        assert invoice.metadata == {"key": "value"}
        assert invoice.url == "https://example.com/invoice/123456789"
