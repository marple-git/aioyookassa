from typing import Any, Dict, Optional

from aioyookassa.core.utils import remove_none_values
from aioyookassa.types.params import PayoutReceiptData
from aioyookassa.types.payout import SelfEmployed

from .base import APIMethod, BaseAPIMethod


class PayoutsAPIMethod(BaseAPIMethod):
    """
    Base class for payouts API methods.
    """

    http_method = "GET"
    path = "/payouts"

    @classmethod
    def build(cls, payout_id: str) -> "PayoutsAPIMethod":  # type: ignore[override]
        """
        Build method for payout-specific endpoints.

        :param payout_id: Payout ID
        :return: Method instance
        """
        result = super().build(payout_id=payout_id)
        return result  # type: ignore[return-value]


class CreatePayout(PayoutsAPIMethod):
    """
    Create payout.
    """

    http_method = "POST"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        amount = kwargs.get("amount")
        payout_destination_data = kwargs.get("payout_destination_data")
        deal = kwargs.get("deal")
        self_employed = kwargs.get("self_employed")
        receipt_data = kwargs.get("receipt_data")

        params = {
            "amount": APIMethod._safe_model_dump(amount, exclude_none=True),
            "payout_destination_data": APIMethod._safe_model_dump(
                payout_destination_data, exclude_none=True
            ),
            "payout_token": kwargs.get("payout_token"),
            "payment_method_id": kwargs.get("payment_method_id"),
            "description": kwargs.get("description"),
            "deal": APIMethod._safe_model_dump(deal, exclude_none=True),
            "self_employed": APIMethod._safe_model_dump(
                self_employed, exclude_none=True
            ),
            "receipt_data": APIMethod._safe_model_dump(receipt_data, exclude_none=True),
            "personal_data": kwargs.get("personal_data"),
            "metadata": kwargs.get("metadata"),
        }
        return remove_none_values(params)


class GetPayout(PayoutsAPIMethod):
    """
    Get payout.
    """

    http_method = "GET"
    path = "/payouts/{payout_id}"
