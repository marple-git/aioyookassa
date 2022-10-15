import abc
from typing import Optional, Type, Union, Callable

from aiohttp import ClientSession, BasicAuth

from aioyookassa.core.methods.base import APIMethod
from aioyookassa.exceptions.base import APIError


class BaseAPIClient(abc.ABC):
    """
    Base API Client
    """
    BASE_URL = 'https://api.yookassa.ru/v3'

    def __init__(self, api_key: str, shop_id: Union[int, str]):
        self.api_key = api_key
        self.shop_id = str(shop_id)

    async def _send_request(self, method: Type[APIMethod],
                            json: Optional[dict] = None,
                            params: Optional[dict] = None,
                            headers: Optional[dict] = None) -> dict:
        """
        Send request to the API
        :param method: API Method
        :param params: Parameters
        :return: JSON
        """
        async with ClientSession() as session:
            params = self._delete_none(params or {})
            json = self._delete_none(json or {})
            request_url = self._get_request_url(method)
            request_headers = {'Content-Type': 'application/json'}

            request_headers.update(headers or {})

            response = await session.request(
                method.http_method,
                request_url,
                json=json,
                params=params,
                headers=request_headers,
                auth=BasicAuth(self.shop_id, self.api_key)
            )

            response_json = await response.json()

            if response.status != 200:
                APIError.detect(response_json['code'], response_json['description'])

            return response_json

    def _get_request_url(self, method: Type[APIMethod]) -> str:
        """
        Get url to send a request
        :param method: Method
        :return: URL
        """
        return f'{self.BASE_URL}{method.path}'

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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        return None
