from typing import Any, Dict

from .base import BaseAPIMethod


class SbpBanksAPIMethod(BaseAPIMethod):
    """
    Base class for SBP banks API methods.
    """

    http_method = "GET"
    path = "/sbp_banks"


class GetSbpBanks(SbpBanksAPIMethod):
    """
    Get SBP banks list.
    """

    http_method = "GET"

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        """
        Build params for GET /sbp_banks request.
        No parameters required.
        """
        return {}
