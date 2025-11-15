from typing import Any, Dict

from aioyookassa.types.params import SelfEmployedConfirmationData

from .base import APIMethod, BaseAPIMethod


class SelfEmployedAPIMethod(BaseAPIMethod):
    """
    Base class for self-employed API methods.
    """

    http_method = "GET"
    path = "/self_employed"

    @classmethod
    def build(cls, self_employed_id: str) -> "SelfEmployedAPIMethod":  # type: ignore[override]
        """
        Build method for self-employed-specific endpoints.

        :param self_employed_id: Self-employed ID
        :return: Method instance
        """
        result = super().build(self_employed_id=self_employed_id)
        return result  # type: ignore[return-value]


class CreateSelfEmployed(SelfEmployedAPIMethod):
    """
    Create self-employed.
    """

    http_method = "POST"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        confirmation = kwargs.get("confirmation")

        params = {
            "itn": kwargs.get("itn"),
            "phone": kwargs.get("phone"),
            "confirmation": APIMethod._safe_model_dump(confirmation, exclude_none=True),
        }
        return {k: v for k, v in params.items() if v is not None}


class GetSelfEmployed(SelfEmployedAPIMethod):
    """
    Get self-employed.
    """

    http_method = "GET"
    path = "/self_employed/{self_employed_id}"
