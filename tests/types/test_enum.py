"""
Tests for enum types.
"""

import pytest

from aioyookassa.types.enum import (
    CancellationParty,
    CancellationReason,
    ConfirmationType,
    Currency,
    DealStatus,
    FeeMoment,
    PaymentMethodType,
    PaymentMode,
    PaymentStatus,
    PaymentSubject,
    PayoutStatus,
    PersonalDataCancellationParty,
    PersonalDataCancellationReason,
    PersonalDataStatus,
    PersonalDataType,
    ReceiptRegistration,
    ReceiptStatus,
    ReceiptType,
    SelfEmployedStatus,
    WebhookEvent,
)


class TestPaymentStatus:
    """Test PaymentStatus enum."""

    def test_payment_status_values(self):
        """Test PaymentStatus enum values."""
        assert PaymentStatus.WAITING_FOR_CAPTURE == "waiting_for_capture"
        assert PaymentStatus.SUCCEEDED == "succeeded"
        assert PaymentStatus.CANCELED == "canceled"
        assert PaymentStatus.PENDING == "pending"

    def test_payment_status_string_representation(self):
        """Test PaymentStatus string representation."""
        assert str(PaymentStatus.SUCCEEDED) == "succeeded"
        assert str(PaymentStatus.CANCELED) == "canceled"

    def test_payment_status_equality(self):
        """Test PaymentStatus equality."""
        assert PaymentStatus.SUCCEEDED == "succeeded"
        assert PaymentStatus.SUCCEEDED != "failed"


class TestConfirmationType:
    """Test ConfirmationType enum."""

    def test_confirmation_type_values(self):
        """Test ConfirmationType enum values."""
        assert ConfirmationType.REDIRECT == "redirect"
        assert ConfirmationType.EXTERNAL == "external"
        assert ConfirmationType.EMBEDDED == "embedded"
        assert ConfirmationType.MOBILE_APPLICATION == "mobile_application"
        assert ConfirmationType.QR_CODE == "qr"

    def test_confirmation_type_string_representation(self):
        """Test ConfirmationType string representation."""
        assert str(ConfirmationType.REDIRECT) == "redirect"
        assert str(ConfirmationType.QR_CODE) == "qr"


class TestCurrency:
    """Test Currency enum."""

    def test_currency_values(self):
        """Test Currency enum values."""
        assert Currency.RUB == "RUB"
        assert Currency.USD == "USD"
        assert Currency.EUR == "EUR"
        assert Currency.GBP == "GBP"
        assert Currency.CNY == "CNY"
        assert Currency.KZT == "KZT"
        assert Currency.UAH == "UAH"
        assert Currency.BYN == "BYN"

    def test_currency_string_representation(self):
        """Test Currency string representation."""
        assert str(Currency.RUB) == "RUB"
        assert str(Currency.USD) == "USD"


class TestPaymentMethodType:
    """Test PaymentMethodType enum."""

    def test_payment_method_type_values(self):
        """Test PaymentMethodType enum values."""
        assert PaymentMethodType.CARD == "bank_card"
        assert PaymentMethodType.YOO_MONEY == "yoo_money"
        assert PaymentMethodType.QIWI == "qiwi"
        assert PaymentMethodType.SBERBANK == "sberbank"
        assert PaymentMethodType.ALFABANK == "alfabank"
        assert PaymentMethodType.TINKOFF_BANK == "tinkoff_bank"
        assert PaymentMethodType.B2B_SBERBANK == "b2b_sberbank"
        assert PaymentMethodType.SBP == "sbp"
        assert PaymentMethodType.MOBILE_BALANCE == "mobile_balance"
        assert PaymentMethodType.CASH == "cash"
        assert PaymentMethodType.INSTALLMENTS == "installments"

    def test_payment_method_type_string_representation(self):
        """Test PaymentMethodType string representation."""
        assert str(PaymentMethodType.CARD) == "bank_card"
        assert str(PaymentMethodType.YOO_MONEY) == "yoo_money"


class TestPaymentSubject:
    """Test PaymentSubject enum."""

    def test_payment_subject_values(self):
        """Test PaymentSubject enum values."""
        assert PaymentSubject.COMMODITY == "commodity"
        assert PaymentSubject.JOB == "job"
        assert PaymentSubject.SERVICE == "service"
        assert PaymentSubject.PAYMENT == "payment"
        assert PaymentSubject.CASINO == "casino"
        assert PaymentSubject.GAMBLING_BET == "gambling_bet"
        assert PaymentSubject.GAMBLING_PRIZE == "gambling_prize"
        assert PaymentSubject.LOTTERY == "lottery"
        assert PaymentSubject.LOTTERY_PRIZE == "lottery_prize"
        assert PaymentSubject.INTELLECTUAL_ACTIVITY == "intellectual_activity"
        assert PaymentSubject.AGENT_COMMISSION == "agent_commission"
        assert PaymentSubject.PROPERTY_RIGHT == "property_right"
        assert PaymentSubject.NON_OPERATING_GAIN == "non_operating_gain"
        assert PaymentSubject.INSURANCE_PREMIUM == "insurance_premium"
        assert PaymentSubject.SALES_TAX == "sales_tax"
        assert PaymentSubject.RESORT_FEE == "resort_fee"
        assert PaymentSubject.MARKED == "marked"
        assert PaymentSubject.NON_MARKED == "non_marked"
        assert PaymentSubject.FINE == "fine"
        assert PaymentSubject.TAX == "tax"
        assert PaymentSubject.LIEN == "lien"
        assert PaymentSubject.COST == "cost"
        assert PaymentSubject.AGENT_WITHDRAWALS == "agent_withdrawals"
        assert (
            PaymentSubject.PENSION_INSURANCE_WITHOUT_PAYOUTS
            == "pension_insurance_without_payouts"
        )
        assert (
            PaymentSubject.PENSION_INSURANCE_WITH_PAYOUTS
            == "pension_insurance_with_payouts"
        )
        assert (
            PaymentSubject.HEALTH_INSURANCE_WITHOUT_PAYOUTS
            == "health_insurance_without_payouts"
        )
        assert (
            PaymentSubject.HEALTH_INSURANCE_WITH_PAYOUTS
            == "health_insurance_with_payouts"
        )
        assert PaymentSubject.HEALTH_INSURANCE == "health_insurance"
        assert PaymentSubject.ANOTHER == "another"

    def test_payment_subject_string_representation(self):
        """Test PaymentSubject string representation."""
        assert str(PaymentSubject.COMMODITY) == "commodity"
        assert str(PaymentSubject.SERVICE) == "service"


class TestPaymentMode:
    """Test PaymentMode enum."""

    def test_payment_mode_values(self):
        """Test PaymentMode enum values."""
        assert PaymentMode.FULL_PREPAYMENT == "full_prepayment"
        assert PaymentMode.FULL_PAYMENT == "full_payment"

    def test_payment_mode_string_representation(self):
        """Test PaymentMode string representation."""
        assert str(PaymentMode.FULL_PREPAYMENT) == "full_prepayment"
        assert str(PaymentMode.FULL_PAYMENT) == "full_payment"


class TestReceiptRegistration:
    """Test ReceiptRegistration enum."""

    def test_receipt_registration_values(self):
        """Test ReceiptRegistration enum values."""
        assert ReceiptRegistration.SUCCEEDED == "succeeded"
        assert ReceiptRegistration.PENDING == "pending"
        assert ReceiptRegistration.CANCELED == "canceled"

    def test_receipt_registration_string_representation(self):
        """Test ReceiptRegistration string representation."""
        assert str(ReceiptRegistration.SUCCEEDED) == "succeeded"
        assert str(ReceiptRegistration.PENDING) == "pending"


class TestCancellationParty:
    """Test CancellationParty enum."""

    def test_cancellation_party_values(self):
        """Test CancellationParty enum values."""
        assert CancellationParty.MERCHANT == "merchant"
        assert CancellationParty.PAYMENT_NETWORK == "payment_network"
        assert CancellationParty.YOO_MONEY == "yoo_money"

    def test_cancellation_party_string_representation(self):
        """Test CancellationParty string representation."""
        assert str(CancellationParty.MERCHANT) == "merchant"
        assert str(CancellationParty.PAYMENT_NETWORK) == "payment_network"


class TestCancellationReason:
    """Test CancellationReason enum."""

    def test_cancellation_reason_values(self):
        """Test CancellationReason enum values."""
        assert CancellationReason.THREE_DS_CHECK_FAILED == "3d_secure_failed"
        assert CancellationReason.CALL_ISSUER == "call_issuer"
        assert CancellationReason.CANCELED_BY_MERCHANT == "canceled_by_merchant"
        assert CancellationReason.CARD_EXPIRED == "card_expired"
        assert CancellationReason.COUNTRY_FORBIDDEN == "country_forbidden"
        assert CancellationReason.DEAL_EXPIRED == "deal_expired"
        assert CancellationReason.EXPIRED_ON_CAPTURE == "expired_on_capture"
        assert CancellationReason.EXPIRED_ON_CONFIRMATION == "expired_on_confirmation"
        assert CancellationReason.FRAUD_SUSPECTED == "fraud_suspected"
        assert CancellationReason.GENERAL_DECLINE == "general_decline"
        assert CancellationReason.IDENTIFICATION_REQUIRED == "identification_required"
        assert CancellationReason.INSUFFICIENT_FUNDS == "insufficient_funds"
        assert CancellationReason.INTERNAL_TIMEOUT == "internal_timeout"
        assert CancellationReason.INVALID_CARD_NUMBER == "invalid_card_number"
        assert CancellationReason.INVALID_CSC == "invalid_csc"
        assert CancellationReason.ISSUER_UNAVAILABLE == "issuer_unavailable"
        assert (
            CancellationReason.PAYMENT_METHOD_LIMIT_EXCEEDED
            == "payment_method_limit_exceeded"
        )
        assert (
            CancellationReason.PAYMENT_METHOD_RESTRICTED == "payment_method_restricted"
        )
        assert CancellationReason.PERMISSION_REVOKED == "permission_revoked"
        assert (
            CancellationReason.UNSUPPORTED_MOBILE_OPERATOR
            == "unsupported_mobile_operator"
        )

    def test_cancellation_reason_string_representation(self):
        """Test CancellationReason string representation."""
        assert str(CancellationReason.THREE_DS_CHECK_FAILED) == "3d_secure_failed"
        assert str(CancellationReason.CALL_ISSUER) == "call_issuer"


class TestReceiptType:
    """Test ReceiptType enum."""

    def test_receipt_type_values(self):
        """Test ReceiptType enum values."""
        assert ReceiptType.PAYMENT == "payment"
        assert ReceiptType.REFUND == "refund"

    def test_receipt_type_string_representation(self):
        """Test ReceiptType string representation."""
        assert str(ReceiptType.PAYMENT) == "payment"
        assert str(ReceiptType.REFUND) == "refund"


class TestReceiptStatus:
    """Test ReceiptStatus enum."""

    def test_receipt_status_values(self):
        """Test ReceiptStatus enum values."""
        assert ReceiptStatus.PENDING == "pending"
        assert ReceiptStatus.SUCCEEDED == "succeeded"
        assert ReceiptStatus.CANCELED == "canceled"

    def test_receipt_status_string_representation(self):
        """Test ReceiptStatus string representation."""
        assert str(ReceiptStatus.PENDING) == "pending"
        assert str(ReceiptStatus.SUCCEEDED) == "succeeded"


class TestPayoutStatus:
    """Test PayoutStatus enum."""

    def test_payout_status_values(self):
        """Test PayoutStatus enum values."""
        assert PayoutStatus.PENDING == "pending"
        assert PayoutStatus.SUCCEEDED == "succeeded"
        assert PayoutStatus.CANCELED == "canceled"

    def test_payout_status_string_representation(self):
        """Test PayoutStatus string representation."""
        assert str(PayoutStatus.PENDING) == "pending"
        assert str(PayoutStatus.SUCCEEDED) == "succeeded"
        assert str(PayoutStatus.CANCELED) == "canceled"

    def test_payout_status_equality(self):
        """Test PayoutStatus equality."""
        assert PayoutStatus.SUCCEEDED == "succeeded"
        assert PayoutStatus.PENDING == "pending"
        assert PayoutStatus.CANCELED == "canceled"


class TestSelfEmployedStatus:
    """Test SelfEmployedStatus enum."""

    def test_self_employed_status_values(self):
        """Test SelfEmployedStatus enum values."""
        assert SelfEmployedStatus.PENDING == "pending"
        assert SelfEmployedStatus.CONFIRMED == "confirmed"
        assert SelfEmployedStatus.CANCELED == "canceled"
        assert SelfEmployedStatus.UNREGISTERED == "unregistered"

    def test_self_employed_status_string_representation(self):
        """Test SelfEmployedStatus string representation."""
        assert str(SelfEmployedStatus.PENDING) == "pending"
        assert str(SelfEmployedStatus.CONFIRMED) == "confirmed"
        assert str(SelfEmployedStatus.CANCELED) == "canceled"
        assert str(SelfEmployedStatus.UNREGISTERED) == "unregistered"

    def test_self_employed_status_equality(self):
        """Test SelfEmployedStatus equality."""
        assert SelfEmployedStatus.CONFIRMED == "confirmed"
        assert SelfEmployedStatus.PENDING == "pending"
        assert SelfEmployedStatus.CANCELED == "canceled"
        assert SelfEmployedStatus.UNREGISTERED == "unregistered"


class TestPersonalDataType:
    """Test PersonalDataType enum."""

    def test_personal_data_type_values(self):
        """Test PersonalDataType enum values."""
        assert PersonalDataType.SBP_PAYOUT_RECIPIENT == "sbp_payout_recipient"
        assert (
            PersonalDataType.PAYOUT_STATEMENT_RECIPIENT == "payout_statement_recipient"
        )

    def test_personal_data_type_string_representation(self):
        """Test PersonalDataType string representation."""
        assert str(PersonalDataType.SBP_PAYOUT_RECIPIENT) == "sbp_payout_recipient"
        assert (
            str(PersonalDataType.PAYOUT_STATEMENT_RECIPIENT)
            == "payout_statement_recipient"
        )

    def test_personal_data_type_equality(self):
        """Test PersonalDataType equality."""
        assert PersonalDataType.SBP_PAYOUT_RECIPIENT == "sbp_payout_recipient"
        assert (
            PersonalDataType.PAYOUT_STATEMENT_RECIPIENT == "payout_statement_recipient"
        )


class TestPersonalDataStatus:
    """Test PersonalDataStatus enum."""

    def test_personal_data_status_values(self):
        """Test PersonalDataStatus enum values."""
        assert PersonalDataStatus.WAITING_FOR_OPERATION == "waiting_for_operation"
        assert PersonalDataStatus.ACTIVE == "active"
        assert PersonalDataStatus.CANCELED == "canceled"

    def test_personal_data_status_string_representation(self):
        """Test PersonalDataStatus string representation."""
        assert str(PersonalDataStatus.WAITING_FOR_OPERATION) == "waiting_for_operation"
        assert str(PersonalDataStatus.ACTIVE) == "active"
        assert str(PersonalDataStatus.CANCELED) == "canceled"

    def test_personal_data_status_equality(self):
        """Test PersonalDataStatus equality."""
        assert PersonalDataStatus.WAITING_FOR_OPERATION == "waiting_for_operation"
        assert PersonalDataStatus.ACTIVE == "active"
        assert PersonalDataStatus.CANCELED == "canceled"


class TestPersonalDataCancellationParty:
    """Test PersonalDataCancellationParty enum."""

    def test_personal_data_cancellation_party_values(self):
        """Test PersonalDataCancellationParty enum values."""
        assert PersonalDataCancellationParty.YOO_MONEY == "yoo_money"

    def test_personal_data_cancellation_party_string_representation(self):
        """Test PersonalDataCancellationParty string representation."""
        assert str(PersonalDataCancellationParty.YOO_MONEY) == "yoo_money"

    def test_personal_data_cancellation_party_equality(self):
        """Test PersonalDataCancellationParty equality."""
        assert PersonalDataCancellationParty.YOO_MONEY == "yoo_money"


class TestPersonalDataCancellationReason:
    """Test PersonalDataCancellationReason enum."""

    def test_personal_data_cancellation_reason_values(self):
        """Test PersonalDataCancellationReason enum values."""
        assert PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT == "expired_by_timeout"

    def test_personal_data_cancellation_reason_string_representation(self):
        """Test PersonalDataCancellationReason string representation."""
        assert (
            str(PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT)
            == "expired_by_timeout"
        )

    def test_personal_data_cancellation_reason_equality(self):
        """Test PersonalDataCancellationReason equality."""
        assert PersonalDataCancellationReason.EXPIRED_BY_TIMEOUT == "expired_by_timeout"


class TestDealStatus:
    """Test DealStatus enum."""

    def test_deal_status_values(self):
        """Test DealStatus enum values."""
        assert DealStatus.OPENED == "opened"
        assert DealStatus.CLOSED == "closed"

    def test_deal_status_string_representation(self):
        """Test DealStatus string representation."""
        assert str(DealStatus.OPENED) == "opened"
        assert str(DealStatus.CLOSED) == "closed"

    def test_deal_status_equality(self):
        """Test DealStatus equality."""
        assert DealStatus.OPENED == "opened"
        assert DealStatus.CLOSED == "closed"


class TestFeeMoment:
    """Test FeeMoment enum."""

    def test_fee_moment_values(self):
        """Test FeeMoment enum values."""
        assert FeeMoment.PAYMENT_SUCCEEDED == "payment_succeeded"
        assert FeeMoment.DEAL_CLOSED == "deal_closed"

    def test_fee_moment_string_representation(self):
        """Test FeeMoment string representation."""
        assert str(FeeMoment.PAYMENT_SUCCEEDED) == "payment_succeeded"
        assert str(FeeMoment.DEAL_CLOSED) == "deal_closed"

    def test_fee_moment_equality(self):
        """Test FeeMoment equality."""
        assert FeeMoment.PAYMENT_SUCCEEDED == "payment_succeeded"
        assert FeeMoment.DEAL_CLOSED == "deal_closed"


class TestWebhookEvent:
    """Test WebhookEvent enum."""

    def test_webhook_event_values(self):
        """Test WebhookEvent enum values."""
        assert WebhookEvent.PAYMENT_WAITING_FOR_CAPTURE == "payment.waiting_for_capture"
        assert WebhookEvent.PAYMENT_SUCCEEDED == "payment.succeeded"
        assert WebhookEvent.PAYMENT_CANCELED == "payment.canceled"
        assert WebhookEvent.PAYMENT_METHOD_ACTIVE == "payment_method.active"
        assert WebhookEvent.REFUND_SUCCEEDED == "refund.succeeded"
        assert WebhookEvent.PAYOUT_SUCCEEDED == "payout.succeeded"
        assert WebhookEvent.PAYOUT_CANCELED == "payout.canceled"
        assert WebhookEvent.DEAL_CLOSED == "deal.closed"

    def test_webhook_event_string_representation(self):
        """Test WebhookEvent string representation."""
        assert (
            str(WebhookEvent.PAYMENT_WAITING_FOR_CAPTURE)
            == "payment.waiting_for_capture"
        )
        assert str(WebhookEvent.PAYMENT_SUCCEEDED) == "payment.succeeded"
        assert str(WebhookEvent.PAYMENT_CANCELED) == "payment.canceled"
        assert str(WebhookEvent.PAYMENT_METHOD_ACTIVE) == "payment_method.active"
        assert str(WebhookEvent.REFUND_SUCCEEDED) == "refund.succeeded"
        assert str(WebhookEvent.PAYOUT_SUCCEEDED) == "payout.succeeded"
        assert str(WebhookEvent.PAYOUT_CANCELED) == "payout.canceled"
        assert str(WebhookEvent.DEAL_CLOSED) == "deal.closed"

    def test_webhook_event_equality(self):
        """Test WebhookEvent equality."""
        assert WebhookEvent.PAYMENT_WAITING_FOR_CAPTURE == "payment.waiting_for_capture"
        assert WebhookEvent.PAYMENT_SUCCEEDED == "payment.succeeded"
        assert WebhookEvent.PAYMENT_CANCELED == "payment.canceled"
        assert WebhookEvent.PAYMENT_METHOD_ACTIVE == "payment_method.active"
        assert WebhookEvent.REFUND_SUCCEEDED == "refund.succeeded"
        assert WebhookEvent.PAYOUT_SUCCEEDED == "payout.succeeded"
        assert WebhookEvent.PAYOUT_CANCELED == "payout.canceled"
        assert WebhookEvent.DEAL_CLOSED == "deal.closed"
