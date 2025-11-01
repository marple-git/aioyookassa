from typing import Any, Dict, Optional

from .base import APIMethod


class GetMe(APIMethod):
    """
    Get shop or gateway settings information.

    API reference: https://yookassa.ru/developers/api#me
    """

    http_method = "GET"
    path = "/me"

    @staticmethod
    def build_params(
        on_behalf_of: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Build query parameters for GET /me request.

        :param on_behalf_of: Shop ID for Split payments
        :param kwargs: Additional parameters
        :return: Query parameters dict
        """
        params: Dict[str, Any] = {}
        if on_behalf_of:
            params["on_behalf_of"] = on_behalf_of
        return params
