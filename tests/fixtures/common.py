"""
Common test fixtures for aioyookassa tests.
"""

import datetime
from decimal import Decimal
from typing import Any, Dict

import pytest

from aioyookassa.types import (
    CardInfo,
    Confirmation,
    Customer,
    Invoice,
    InvoiceCartItem,
    InvoiceReceipt,
    InvoiceReceiptItem,
    Payment,
    PaymentAmount,
    PaymentItem,
    PaymentMethod,
    PaymentsList,
    Receipt,
    Recipient,
    Refund,
    RefundDeal,
    RefundSettlement,
    RefundsList,
    RefundSource,
)
from aioyookassa.types.enum import (
    CancellationParty,
    CancellationReason,
    ConfirmationType,
    Currency,
    PaymentMethodType,
    PaymentMode,
    PaymentStatus,
    PaymentSubject,
    ReceiptRegistration,
)


@pytest.fixture
def sample_payment_amount():
    """Sample payment amount fixture."""
    return PaymentAmount(value=100.50, currency=Currency.RUB)


@pytest.fixture
def sample_card_info():
    """Sample card info fixture."""
    return CardInfo(
        last_four="1234", expiry_year="2025", expiry_month="12", card_type="Visa"
    )


@pytest.fixture
def sample_payment_method():
    """Sample payment method fixture."""
    return PaymentMethod(
        type=PaymentMethodType.CARD,
        id="pm_123456789",
        saved=True,
        title="Test Card",
        card=sample_card_info(),
    )


@pytest.fixture
def sample_confirmation():
    """Sample confirmation fixture."""
    return Confirmation(
        type=ConfirmationType.REDIRECT,
        url="https://example.com/confirm",
        return_url="https://example.com/return",
    )


@pytest.fixture
def sample_recipient():
    """Sample recipient fixture."""
    return Recipient(account_id="123456", gateway_id="gateway_123")


@pytest.fixture
def sample_customer():
    """Sample customer fixture."""
    return Customer(full_name="John Doe", email="john@example.com", phone="+1234567890")


@pytest.fixture
def sample_payment_item():
    """Sample payment item fixture."""
    return PaymentItem(
        description="Test item",
        amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        vat_code=1,
        quantity=1,
        payment_subject=PaymentSubject.COMMODITY,
        payment_mode=PaymentMode.FULL_PAYMENT,
    )


@pytest.fixture
def sample_receipt():
    """Sample receipt fixture."""
    return Receipt(
        customer=sample_customer(),
        items=[sample_payment_item()],
        phone="+1234567890",
        email="john@example.com",
    )


@pytest.fixture
def sample_payment():
    """Sample payment fixture."""
    return Payment(
        id="payment_123456789",
        status=PaymentStatus.SUCCEEDED,
        amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        description="Test payment",
        recipient=sample_recipient(),
        payment_method=sample_payment_method(),
        created_at=datetime.datetime.now(),
        test=True,
        paid=True,
        refundable=True,
    )


@pytest.fixture
def sample_payments_list():
    """Sample payments list fixture."""
    return PaymentsList(list=[sample_payment()], cursor="next_cursor_123")


@pytest.fixture
def sample_invoice_cart_item():
    """Sample invoice cart item fixture."""
    return InvoiceCartItem(
        description="Test invoice item",
        price=PaymentAmount(value=100.50, currency=Currency.RUB),
        quantity=1,
    )


@pytest.fixture
def sample_invoice_receipt_item():
    """Sample invoice receipt item fixture."""
    return InvoiceReceiptItem(
        description="Test invoice receipt item",
        amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        vat_code=1,
        quantity=1,
    )


@pytest.fixture
def sample_invoice_receipt():
    """Sample invoice receipt fixture."""
    return InvoiceReceipt(
        customer=sample_customer(), items=[sample_invoice_receipt_item()], internet=True
    )


@pytest.fixture
def sample_invoice():
    """Sample invoice fixture."""
    return Invoice(
        id="invoice_123456789",
        status="active",
        cart=[sample_invoice_cart_item()],
        created_at=datetime.datetime.now(),
        expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
    )


@pytest.fixture
def sample_refund_settlement():
    """Sample refund settlement fixture."""
    return RefundSettlement(
        type="payout", amount=PaymentAmount(value=100.50, currency=Currency.RUB)
    )


@pytest.fixture
def sample_refund_deal():
    """Sample refund deal fixture."""
    return RefundDeal(
        id="deal_123456789", refund_settlements=[sample_refund_settlement()]
    )


@pytest.fixture
def sample_refund_source():
    """Sample refund source fixture."""
    return RefundSource(
        account_id="123456", amount=PaymentAmount(value=100.50, currency=Currency.RUB)
    )


@pytest.fixture
def sample_refund():
    """Sample refund fixture."""
    return Refund(
        id="refund_123456789",
        payment_id="payment_123456789",
        status="succeeded",
        amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        created_at=datetime.datetime.now(),
    )


@pytest.fixture
def sample_refunds_list():
    """Sample refunds list fixture."""
    return RefundsList(list=[sample_refund()], next_cursor="next_cursor_123")


@pytest.fixture
def sample_api_response():
    """Sample API response fixture."""
    return {
        "id": "payment_123456789",
        "status": "succeeded",
        "amount": {"value": 100.50, "currency": "RUB"},
        "description": "Test payment",
        "recipient": {"account_id": "123456", "gateway_id": "gateway_123"},
        "payment_method": {
            "type": "bank_card",
            "id": "pm_123456789",
            "saved": True,
            "title": "Test Card",
            "card": {
                "last4": "1234",
                "expiry_year": "2025",
                "expiry_month": "12",
                "card_type": "Visa",
            },
        },
        "created_at": "2023-01-01T00:00:00.000Z",
        "test": True,
        "paid": True,
        "refundable": True,
    }
