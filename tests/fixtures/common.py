"""
Common test fixtures for aioyookassa tests.
"""

import datetime
from decimal import Decimal
from typing import Any, Dict

import pytest

from aioyookassa.types import (
    Airline,
    Confirmation,
    Customer,
    Deal,
    Invoice,
    InvoiceCartItem,
    InvoiceReceipt,
    InvoiceReceiptItem,
    Payment,
    PaymentAmount,
    PaymentItem,
    PaymentsList,
    Receipt,
    Refund,
    RefundDeal,
    RefundsList,
    RefundSource,
    Transfer,
)
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
    PayoutStatus,
    ReceiptRegistration,
    SelfEmployedStatus,
)
from aioyookassa.types.payment import CardInfo, PaymentMethod, Recipient, Settlement
from aioyookassa.types.payout import (
    BankCardPayoutDestination,
    Payout,
    PayoutCardInfo,
    SelfEmployed,
    SelfEmployedConfirmation,
)
from aioyookassa.types.personal_data import PersonalDataCancellationDetails
from aioyookassa.types.sbp_banks import SbpBanksList, SbpParticipantBank


@pytest.fixture
def sample_payment_amount():
    """Sample payment amount fixture."""
    return PaymentAmount(value=100.50, currency=Currency.RUB)


@pytest.fixture
def sample_card_info():
    """Sample card info fixture."""
    return CardInfo(
        last4="1234", expiry_year="2025", expiry_month="12", card_type="Visa"
    )


@pytest.fixture
def sample_payment_method(sample_card_info):
    """Sample payment method fixture."""
    return PaymentMethod(
        type=PaymentMethodType.CARD,
        id="pm_123456789",
        saved=True,
        status=PaymentMethodStatus.ACTIVE,
        title="Test Card",
        card=sample_card_info,
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
def sample_receipt(sample_customer, sample_payment_item):
    """Sample receipt fixture."""
    return Receipt(
        customer=sample_customer,
        items=[sample_payment_item],
        phone="+1234567890",
        email="john@example.com",
    )


@pytest.fixture
def sample_payment(sample_recipient, sample_payment_method):
    """Sample payment fixture."""
    return Payment(
        id="payment_123456789",
        status=PaymentStatus.SUCCEEDED,
        amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        description="Test payment",
        recipient=sample_recipient,
        payment_method=sample_payment_method,
        created_at=datetime.datetime.now(),
        test=True,
        paid=True,
        refundable=True,
    )


@pytest.fixture
def sample_payments_list(sample_payment):
    """Sample payments list fixture."""
    return PaymentsList(list=[sample_payment], cursor="next_cursor_123")


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
def sample_invoice_receipt(sample_customer, sample_invoice_receipt_item):
    """Sample invoice receipt fixture."""
    return InvoiceReceipt(
        customer=sample_customer, items=[sample_invoice_receipt_item], internet=True
    )


@pytest.fixture
def sample_invoice(sample_invoice_cart_item):
    """Sample invoice fixture."""
    return Invoice(
        id="invoice_123456789",
        status="active",
        cart=[sample_invoice_cart_item],
        created_at=datetime.datetime.now(),
        expires_at=datetime.datetime.now() + datetime.timedelta(days=1),
    )


@pytest.fixture
def sample_refund_settlement():
    """Sample refund settlement fixture."""
    return Settlement(
        type="payout", amount=PaymentAmount(value=100.50, currency=Currency.RUB)
    )


@pytest.fixture
def sample_refund_deal(sample_refund_settlement):
    """Sample refund deal fixture."""
    return RefundDeal(
        id="deal_123456789", refund_settlements=[sample_refund_settlement]
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
def sample_refunds_list(sample_refund):
    """Sample refunds list fixture."""
    return RefundsList(list=[sample_refund], next_cursor="next_cursor_123")


@pytest.fixture
def sample_airline():
    """Sample airline fixture."""
    return Airline(ticket_number="TK123456", booking_reference="ABC123")


@pytest.fixture
def sample_transfer():
    """Sample transfer fixture."""
    return Transfer(
        account_id="123456",
        amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        status=PaymentStatus.SUCCEEDED,
    )


@pytest.fixture
def sample_deal():
    """Sample deal fixture."""
    return Deal(
        id="deal_123456789",
        settlements=[PaymentAmount(value=100.50, currency=Currency.RUB)],
    )


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
            "status": "active",
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


@pytest.fixture
def sample_payout_card_info():
    """Sample payout card info fixture."""
    return PayoutCardInfo(
        first6="123456",
        last4="7890",
        card_type="Visa",
        issuer_country="RU",
        issuer_name="Test Bank",
    )


@pytest.fixture
def sample_payout_destination(sample_payout_card_info):
    """Sample payout destination fixture."""
    return BankCardPayoutDestination(card=sample_payout_card_info)


@pytest.fixture
def sample_payout(sample_payout_destination):
    """Sample payout fixture."""
    return Payout(
        id="payout_123456789",
        status=PayoutStatus.PENDING,
        amount=PaymentAmount(value=100.50, currency=Currency.RUB),
        payout_destination=sample_payout_destination,
        created_at=datetime.datetime.now(),
        test=True,
    )


@pytest.fixture
def sample_payout_deal():
    """Sample payout deal fixture."""
    from aioyookassa.types.payment import Deal

    return Deal(id="deal_123456789")


@pytest.fixture
def sample_self_employed():
    """Sample self-employed fixture (minimal, for use in Payout)."""
    return SelfEmployed(id="se_123456789")


@pytest.fixture
def sample_self_employed_confirmation():
    """Sample self-employed confirmation fixture."""
    return SelfEmployedConfirmation(confirmation_url="https://example.com/confirm")


@pytest.fixture
def sample_self_employed_full(sample_self_employed_confirmation):
    """Sample full self-employed fixture."""
    return SelfEmployed(
        id="se_123456789",
        status=SelfEmployedStatus.CONFIRMED,
        created_at=datetime.datetime.now(),
        itn="123456789012",
        phone="79000000000",
        confirmation=sample_self_employed_confirmation,
        test=True,
    )


@pytest.fixture
def sample_sbp_participant_bank():
    """Sample SBP participant bank fixture."""
    return SbpParticipantBank(bank_id="100000000001", name="Test Bank", bic="044525225")


@pytest.fixture
def sample_sbp_banks_list(sample_sbp_participant_bank):
    """Sample SBP banks list fixture."""
    bank2 = SbpParticipantBank(
        bank_id="100000000002", name="Another Bank", bic="044525226"
    )
    return SbpBanksList(items=[sample_sbp_participant_bank, bank2])


@pytest.fixture
def sample_personal_data_cancellation_details():
    """Sample personal data cancellation details fixture."""
    from aioyookassa.types.enum import (
        PersonalDataCancellationParty,
        PersonalDataCancellationReason,
    )

    return PersonalDataCancellationDetails(
        party=PersonalDataCancellationParty.YOO_MONEY,
        reason=PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT,
    )


@pytest.fixture
def sample_personal_data(sample_personal_data_cancellation_details):
    """Sample personal data fixture."""
    from aioyookassa.types.enum import PersonalDataStatus, PersonalDataType
    from aioyookassa.types.personal_data import PersonalData

    return PersonalData(
        id="pd_123456789",
        type=PersonalDataType.SBP_PAYOUT_RECIPIENT,
        status=PersonalDataStatus.WAITING_FOR_OPERATION,
        created_at=datetime.datetime.now(),
        cancellation_details=sample_personal_data_cancellation_details,
        metadata={"key": "value"},
    )


@pytest.fixture
def sample_personal_data_active():
    """Sample active personal data fixture."""
    from aioyookassa.types.enum import PersonalDataStatus, PersonalDataType
    from aioyookassa.types.personal_data import PersonalData

    return PersonalData(
        id="pd_987654321",
        type=PersonalDataType.PAYOUT_STATEMENT_RECIPIENT,
        status=PersonalDataStatus.ACTIVE,
        created_at=datetime.datetime.now(),
        expires_at=datetime.datetime.now() + datetime.timedelta(days=30),
        metadata={"order_id": "12345"},
    )


# Webhooks fixtures
@pytest.fixture
def sample_webhook_minimal():
    """Sample minimal webhook for testing."""
    from aioyookassa.types.webhooks import Webhook

    return Webhook(
        id="wh_123456789",
        event="payment.succeeded",
        url="https://example.com/webhook",
    )


@pytest.fixture
def sample_webhook_full():
    """Sample full webhook for testing."""
    from aioyookassa.types.webhooks import Webhook

    return Webhook(
        id="wh_987654321",
        event="deal.closed",
        url="https://api.example.com/v1/webhooks",
    )


@pytest.fixture
def sample_webhooks_list(sample_webhook_minimal, sample_webhook_full):
    """Sample webhooks list for testing."""
    from aioyookassa.types.webhooks import WebhooksList

    return WebhooksList(items=[sample_webhook_minimal, sample_webhook_full])
