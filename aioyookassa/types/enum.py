import sys
from enum import Enum
from typing import Any

# StrEnum is available in Python 3.11+, for older versions we use (str, Enum)
if sys.version_info >= (3, 11):
    from enum import StrEnum
else:

    class StrEnum(str, Enum):
        """
        Backport of StrEnum for Python < 3.11
        """

        def __str__(self) -> str:
            return str(self.value)

        def _generate_next_value_(
            name: str, start: int, count: int, last_values: list
        ) -> Any:
            return name.lower()


class PaymentStatus(StrEnum):
    """
    Payment status

    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/getting-started/payment-process#lifecycle
    """

    WAITING_FOR_CAPTURE = "waiting_for_capture"
    SUCCEEDED = "succeeded"
    CANCELED = "canceled"
    PENDING = "pending"


class ConfirmationType(StrEnum):
    """
    Confirmation type

    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/getting-started/payment-process#confirmation
    """

    REDIRECT = "redirect"
    EXTERNAL = "external"
    EMBEDDED = "embedded"
    MOBILE_APPLICATION = "mobile_application"
    QR_CODE = "qr"


class ReceiptRegistration(StrEnum):
    """
    Receipt registration
    """

    SUCCEEDED = "succeeded"
    PENDING = "pending"
    CANCELED = "canceled"


class CancellationParty(StrEnum):
    """
    Cancellation party

    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/after-the-payment/declined-payments#cancellation-details-party
    """

    MERCHANT = "merchant"
    PAYMENT_NETWORK = "payment_network"
    YOO_MONEY = "yoo_money"


class CancellationReason(StrEnum):
    """
    Cancellation reason

    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/after-the-payment/declined-payments#cancellation-details-reason
    """

    THREE_DS_CHECK_FAILED = "3d_secure_failed"
    CALL_ISSUER = "call_issuer"
    CANCELED_BY_MERCHANT = "canceled_by_merchant"
    CARD_EXPIRED = "card_expired"
    COUNTRY_FORBIDDEN = "country_forbidden"
    DEAL_EXPIRED = "deal_expired"
    EXPIRED_ON_CAPTURE = "expired_on_capture"
    EXPIRED_ON_CONFIRMATION = "expired_on_confirmation"
    FRAUD_SUSPECTED = "fraud_suspected"
    GENERAL_DECLINE = "general_decline"
    IDENTIFICATION_REQUIRED = "identification_required"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    INTERNAL_TIMEOUT = "internal_timeout"
    INVALID_CARD_NUMBER = "invalid_card_number"
    INVALID_CSC = "invalid_csc"
    ISSUER_UNAVAILABLE = "issuer_unavailable"
    PAYMENT_METHOD_LIMIT_EXCEEDED = "payment_method_limit_exceeded"
    PAYMENT_METHOD_RESTRICTED = "payment_method_restricted"
    PERMISSION_REVOKED = "permission_revoked"
    UNSUPPORTED_MOBILE_OPERATOR = "unsupported_mobile_operator"


class PaymentMethodType(StrEnum):
    """
    Payment method types
    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/getting-started/payment-methods#all
    """

    CARD = "bank_card"
    YOO_MONEY = "yoo_money"
    QIWI = "qiwi"
    SBERBANK = "sberbank"
    ALFABANK = "alfabank"
    TINKOFF_BANK = "tinkoff_bank"
    B2B_SBERBANK = "b2b_sberbank"
    SBP = "sbp"
    MOBILE_BALANCE = "mobile_balance"
    CASH = "cash"
    INSTALLMENTS = "installments"


class PaymentSubject(StrEnum):
    """
    Payment subject - признак предмета расчета

    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/receipts/54fz/parameters-values#payment-subject
    """

    COMMODITY = "commodity"
    JOB = "job"
    SERVICE = "service"
    PAYMENT = "payment"
    CASINO = "casino"
    GAMBLING_BET = "gambling_bet"
    GAMBLING_PRIZE = "gambling_prize"
    LOTTERY = "lottery"
    LOTTERY_PRIZE = "lottery_prize"
    INTELLECTUAL_ACTIVITY = "intellectual_activity"
    AGENT_COMMISSION = "agent_commission"
    PROPERTY_RIGHT = "property_right"
    NON_OPERATING_GAIN = "non_operating_gain"
    INSURANCE_PREMIUM = "insurance_premium"
    SALES_TAX = "sales_tax"
    RESORT_FEE = "resort_fee"
    MARKED = "marked"
    NON_MARKED = "non_marked"
    FINE = "fine"
    TAX = "tax"
    LIEN = "lien"
    COST = "cost"
    AGENT_WITHDRAWALS = "agent_withdrawals"
    PENSION_INSURANCE_WITHOUT_PAYOUTS = "pension_insurance_without_payouts"
    PENSION_INSURANCE_WITH_PAYOUTS = "pension_insurance_with_payouts"
    HEALTH_INSURANCE_WITHOUT_PAYOUTS = "health_insurance_without_payouts"
    HEALTH_INSURANCE_WITH_PAYOUTS = "health_insurance_with_payouts"
    HEALTH_INSURANCE = "health_insurance"
    ANOTHER = "another"


class PaymentMode(StrEnum):
    """
    Payment mode - признак способа расчета

    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/receipts/54fz/parameters-values#payment-mode
    """

    FULL_PREPAYMENT = "full_prepayment"
    FULL_PAYMENT = "full_payment"


class Currency(StrEnum):
    """
    Currency codes according to ISO 4217

    More detailed documentation:
    https://yookassa.ru/developers/payment-acceptance/basics/payment-process#currency
    """

    RUB = "RUB"  # Russian Ruble
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro
    GBP = "GBP"  # British Pound Sterling
    CNY = "CNY"  # Chinese Yuan
    KZT = "KZT"  # Kazakhstani Tenge
    UAH = "UAH"  # Ukrainian Hryvnia
    BYN = "BYN"  # Belarusian Ruble


class ReceiptType(StrEnum):
    """
    Receipt type for fiscal receipts in online cash register.

    More detailed documentation:
    https://yookassa.ru/developers/api#create_receipt
    """

    PAYMENT = "payment"  # Income receipt
    REFUND = "refund"  # Refund receipt


class ReceiptStatus(StrEnum):
    """
    Receipt registration status.

    More detailed documentation:
    https://yookassa.ru/developers/api#create_receipt
    """

    PENDING = "pending"  # In progress
    SUCCEEDED = "succeeded"  # Successfully registered
    CANCELED = "canceled"  # Canceled
