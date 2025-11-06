"""
Tests for receipt registration types.
"""

import datetime
from decimal import Decimal

import pytest

from aioyookassa.types.enum import ReceiptStatus, ReceiptType
from aioyookassa.types.payment import PaymentAmount, Settlement
from aioyookassa.types.receipt_registration import (
    AdditionalUserProps,
    FiscalReceipt,
    FiscalReceiptsList,
    ReceiptRegistrationItem,
    Supplier,
)


class TestReceiptSettlement:
    """Test Settlement model (used for receipts)."""

    def test_receipt_settlement_creation(self):
        """Test Settlement creation for receipts."""
        settlement = Settlement(
            type="prepayment", amount=PaymentAmount(value=100.50, currency="RUB")
        )
        assert settlement.type == "prepayment"
        assert settlement.amount.value == pytest.approx(100.50)


class TestAdditionalUserProps:
    """Test AdditionalUserProps model."""

    def test_additional_user_props_creation(self):
        """Test AdditionalUserProps creation."""
        props = AdditionalUserProps(name="Test property", value="Test value")
        assert props.name == "Test property"
        assert props.value == "Test value"


class TestSupplier:
    """Test Supplier model."""

    def test_supplier_creation(self):
        """Test Supplier creation."""
        supplier = Supplier(name="Test Supplier", inn="1234567890")
        assert supplier.name == "Test Supplier"
        assert supplier.inn == "1234567890"

    def test_supplier_with_phone(self):
        """Test Supplier with phone."""
        supplier = Supplier(name="Test Supplier", inn="1234567890", phone="+1234567890")
        assert supplier.phone == "+1234567890"


class TestReceiptRegistrationItem:
    """Test ReceiptRegistrationItem model."""

    def test_receipt_registration_item_creation(self):
        """Test ReceiptRegistrationItem creation."""
        item = ReceiptRegistrationItem(
            description="Test receipt item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=1,
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        assert item.description == "Test receipt item"
        assert item.amount.value == pytest.approx(100.50)
        assert item.vat_code == 1
        assert item.quantity == 1
        assert item.payment_subject == "commodity"
        assert item.payment_mode == "full_payment"

    def test_receipt_registration_item_with_optional_fields(self):
        """Test ReceiptRegistrationItem with optional fields."""
        supplier = Supplier(name="Test Supplier", inn="1234567890")

        item = ReceiptRegistrationItem(
            description="Test receipt item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=1,
            payment_subject="commodity",
            payment_mode="full_payment",
            measure="piece",
            country_of_origin_code="RU",
            customs_declaration_number="1234567890",
            excise="0.00",
            product_code="1234567890123",
            mark_mode="unknown",
            mark_quantity={"numerator": 1, "denominator": 2},
            mark_code_info={"unknown": "12345678901234567890"},
            payment_subject_industry_details=[
                {
                    "federal_id": "1234567890",
                    "document_date": "2023-01-01T00:00:00.000Z",
                    "document_number": "DOC123",
                    "value": "Test value",
                }
            ],
            supplier=supplier,
            agent_type="banking_payment_agent",
        )
        assert item.measure == "piece"
        assert item.country_of_origin_code == "RU"
        assert item.customs_declaration_number == "1234567890"
        assert item.excise == "0.00"
        assert item.product_code == "1234567890123"
        assert item.mark_mode == "unknown"
        assert item.mark_quantity.numerator == 1
        assert item.mark_quantity.denominator == 2
        assert item.mark_code_info.unknown == "12345678901234567890"
        assert len(item.payment_subject_industry_details) == 1
        # additional_user_props is not a field in ReceiptRegistrationItem
        assert item.supplier == supplier
        assert item.agent_type == "banking_payment_agent"
        # supplier_phone, supplier_name, supplier_inn are not fields in ReceiptRegistrationItem
        # receipt_industry_details is not a field in ReceiptRegistrationItem
        # receipt_operation_details is not a field in ReceiptRegistrationItem
        # settlements is not a field in ReceiptRegistrationItem

    def test_receipt_registration_item_with_different_quantity_types(self):
        """Test ReceiptRegistrationItem with different quantity types."""
        # Test with int
        item_int = ReceiptRegistrationItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=1,
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        assert item_int.quantity == 1

        # Test with float
        item_float = ReceiptRegistrationItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=1.5,
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        assert item_float.quantity == pytest.approx(1.5)

        # Test with string
        item_string = ReceiptRegistrationItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity="2.5",
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        assert item_string.quantity == "2.5"

        # Test with Decimal
        item_decimal = ReceiptRegistrationItem(
            description="Test item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=Decimal("3.75"),
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        assert item_decimal.quantity == Decimal("3.75")


class TestFiscalReceipt:
    """Test FiscalReceipt model."""

    def test_fiscal_receipt_creation(self):
        """Test FiscalReceipt creation."""
        item = ReceiptRegistrationItem(
            description="Test receipt item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=1,
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        receipt = FiscalReceipt(
            id="receipt_123456789",
            type=ReceiptType.PAYMENT,
            status=ReceiptStatus.SUCCEEDED,
            fiscal_document_number="1234567890",
            fiscal_storage_number="1234567890",
            fiscal_attribute="1234567890",
            registered_at=datetime.datetime.now(),
            items=[item],
        )
        assert receipt.id == "receipt_123456789"
        assert receipt.type == ReceiptType.PAYMENT
        assert receipt.status == ReceiptStatus.SUCCEEDED
        assert receipt.fiscal_document_number == "1234567890"
        assert receipt.fiscal_storage_number == "1234567890"
        assert receipt.fiscal_attribute == "1234567890"
        assert len(receipt.items) == 1

    def test_fiscal_receipt_with_optional_fields(self):
        """Test FiscalReceipt with optional fields."""
        item = ReceiptRegistrationItem(
            description="Test receipt item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=1,
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        settlement = Settlement(
            type="prepayment", amount=PaymentAmount(value=100.50, currency="RUB")
        )

        receipt = FiscalReceipt(
            id="receipt_123456789",
            type=ReceiptType.PAYMENT,
            status=ReceiptStatus.SUCCEEDED,
            fiscal_document_number="1234567890",
            fiscal_storage_number="1234567890",
            fiscal_attribute="1234567890",
            registered_at=datetime.datetime.now(),
            items=[item],
            customer={"email": "test@example.com", "phone": "+1234567890"},
            tax_system_code=1,
            internet=True,
            timezone=3,
            settlements=[settlement],
            receipt_industry_details=[
                {
                    "federal_id": "1234567890",
                    "document_date": "2023-01-01T00:00:00.000Z",
                    "document_number": "DOC123",
                    "value": "Test value",
                }
            ],
            receipt_operational_details={
                "operation_id": 123456,
                "value": "Test value",
                "created_at": "2023-01-01T00:00:00.000Z",
            },
        )
        # Customer is not a field in FiscalReceipt, it's in the items
        assert receipt.tax_system_code == 1
        assert receipt.internet is True
        assert receipt.timezone == 3
        assert len(receipt.settlements) == 1
        # on_demand is not a field in FiscalReceipt
        # additional_user_props is not a field in FiscalReceipt
        assert len(receipt.receipt_industry_details) == 1
        assert receipt.receipt_operational_details.id == 123456
        assert receipt.receipt_operational_details.value == "Test value"
        assert receipt.receipt_operational_details.created_at is not None
        # metadata is not a field in FiscalReceipt


class TestFiscalReceiptsList:
    """Test FiscalReceiptsList model."""

    def test_fiscal_receipts_list_creation(self):
        """Test FiscalReceiptsList creation."""
        item = ReceiptRegistrationItem(
            description="Test receipt item",
            amount=PaymentAmount(value=100.50, currency="RUB"),
            vat_code=1,
            quantity=1,
            payment_subject="commodity",
            payment_mode="full_payment",
        )
        receipt = FiscalReceipt(
            id="receipt_123456789",
            type=ReceiptType.PAYMENT,
            status=ReceiptStatus.SUCCEEDED,
            fiscal_document_number="1234567890",
            fiscal_storage_number="1234567890",
            fiscal_attribute="1234567890",
            registered_at=datetime.datetime.now(),
            items=[item],
        )
        receipts_list = FiscalReceiptsList(
            items=[receipt], next_cursor="next_cursor_123"
        )
        assert len(receipts_list.items) == 1
        assert receipts_list.next_cursor == "next_cursor_123"

    def test_fiscal_receipts_list_with_alias(self):
        """Test FiscalReceiptsList with alias field."""
        receipt_data = {
            "id": "receipt_123456789",
            "type": "payment",
            "status": "succeeded",
            "fiscal_document_number": "1234567890",
            "fiscal_storage_number": "1234567890",
            "fiscal_attribute": "1234567890",
            "registered_at": "2023-01-01T00:00:00.000Z",
            "items": [
                {
                    "description": "Test receipt item",
                    "amount": {"value": "100.50", "currency": "RUB"},
                    "vat_code": 1,
                    "quantity": 1,
                    "payment_subject": "commodity",
                    "payment_mode": "full_payment",
                }
            ],
        }
        receipts_data = {"items": [receipt_data], "next_cursor": "next_cursor_123"}
        receipts_list = FiscalReceiptsList(**receipts_data)
        assert len(receipts_list.items) == 1
        assert receipts_list.next_cursor == "next_cursor_123"
