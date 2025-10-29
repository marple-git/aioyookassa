import abc
from typing import Any, Optional, Type, Union

from aiohttp import BasicAuth, ClientError, ClientSession

from aioyookassa.core.methods.base import APIMethod
from aioyookassa.exceptions import (  # Import from __init__ to register all subclasses
    APIError,
)


class BaseAPIClient(abc.ABC):
    """
    Base API Client
    """

    BASE_URL = "https://api.yookassa.ru/v3"

    def __init__(self, api_key: str, shop_id: Union[int, str]):
        self.api_key = api_key
        self.shop_id = str(shop_id)
        self._session: Optional[ClientSession] = None

    async def _get_session(self) -> ClientSession:
        """
        Get or create aiohttp ClientSession
        :return: ClientSession
        """
        if self._session is None or self._session.closed:
            self._session = ClientSession()
        return self._session

    async def close(self) -> None:
        """
        Close aiohttp session
        """
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _send_request(
        self,
        method: Type[APIMethod],
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> dict:
        """
        Send request to the API
        :param method: API Method
        :param json: JSON data
        :param params: Query parameters
        :param headers: Additional headers
        :return: JSON response
        """
        session = await self._get_session()

        params = self._delete_none(params or {})
        json = self._delete_none(json or {})
        request_url = self._get_request_url(method)
        request_headers = {"Content-Type": "application/json"}

        request_headers.update(headers or {})

        try:
            response = await session.request(
                method.http_method,
                request_url,
                json=json,
                params=params,
                headers=request_headers,
                auth=BasicAuth(self.shop_id, self.api_key),
            )

            # Handle HTTP errors
            if response.status >= 400:
                try:
                    error_data = await response.json()
                except Exception:
                    # Failed to parse JSON, fallback to text
                    error_text = await response.text()
                    raise APIError(f"HTTP {response.status}: {error_text}")

                # Detect and raise the appropriate exception
                APIError.detect(
                    error_data.get("code", "unknown_error"),
                    error_data.get("description", f"HTTP {response.status}"),
                )

            # Parse successful response
            try:
                response_json = await response.json()
            except Exception as e:
                raise APIError(f"Failed to parse JSON response: {str(e)}")

            return response_json  # type: ignore[no-any-return]

        except ClientError as e:
            raise APIError(f"Network error: {str(e)}")

    def _get_request_url(self, method: Type[APIMethod]) -> str:
        """
        Get url to send a request
        :param method: Method
        :return: URL
        """
        return f"{self.BASE_URL}{method.path}"

    def _delete_none(self, _dict: dict) -> dict:
        """Delete None values recursively from all the dictionaries"""
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                self._delete_none(value)
            elif value is None:
                del _dict[key]
            elif isinstance(value, list):
                for v_i in value:
                    if isinstance(v_i, dict):
                        self._delete_none(v_i)

        return _dict

    async def __aenter__(self) -> "BaseAPIClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
