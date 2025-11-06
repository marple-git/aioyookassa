"""
Base API client class for common operations.
"""

from typing import Any, Generic, Optional, Type, TypeVar, Union

from pydantic import BaseModel

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods.base import APIMethod
from aioyookassa.core.utils import create_idempotence_headers, normalize_params

T = TypeVar("T")
TParams = TypeVar("TParams", bound=BaseModel)
TResult = TypeVar("TResult", bound=BaseModel)


class BaseAPI(Generic[TParams, TResult]):
    """
    Base API client class with common operations.

    Provides reusable methods for creating, retrieving, and listing resources.
    """

    def __init__(self, client: BaseAPIClient):
        """
        Initialize base API client.

        :param client: Base API client instance.
        """
        self._client = client

    async def _create_resource(
        self,
        params: Union[TParams, dict],
        params_class: Type[TParams],
        method_class: Type[APIMethod],
        result_class: Type[TResult],
    ) -> TResult:
        """
        Create a resource using the specified method.

        :param params: Creation parameters (Pydantic model or dict).
        :param params_class: Pydantic model class for parameters.
        :param method_class: API method class to use.
        :param result_class: Result model class.
        :returns: Created resource instance.
        """
        params_dict = normalize_params(params, params_class)
        json_data = method_class.build_params(**params_dict)
        headers = create_idempotence_headers()
        result = await self._client._send_request(
            method_class, json=json_data, headers=headers
        )
        return result_class(**result)

    async def _get_list(
        self,
        params: Optional[Union[TParams, dict]],
        params_class: Optional[Type[TParams]],
        method_class: Type[APIMethod],
        result_class: Type[TResult],
        **kwargs: Any,
    ) -> TResult:
        """
        Get a list of resources with optional filtering.

        :param params: Filter parameters (Pydantic model or dict).
        :param params_class: Optional Pydantic model class for parameters.
        :param method_class: API method class to use.
        :param result_class: Result model class.
        :param kwargs: Additional parameters (merged with params).
        :returns: List of resources.
        """
        params_dict = normalize_params(params, params_class)
        params_dict.update(kwargs)
        request_params = method_class.build_params(**params_dict)
        result = await self._client._send_request(method_class, params=request_params)
        return result_class(**result)

    async def _get_by_id(
        self,
        resource_id: str,
        method_class: Type[APIMethod],
        result_class: Type[TResult],
        id_param_name: str = "id",
    ) -> TResult:
        """
        Get a resource by its ID.

        :param resource_id: Resource identifier.
        :param method_class: API method class to use.
        :param result_class: Result model class.
        :param id_param_name: Name of the ID parameter in build method (default: "id").
        :returns: Resource instance.
        """
        method = method_class.build(**{id_param_name: resource_id})
        result = await self._client._send_request(method)
        return result_class(**result)

    async def _update_resource(
        self,
        resource_id: str,
        params: Optional[Union[TParams, dict]],
        params_class: Optional[Type[TParams]],
        method_class: Type[APIMethod],
        result_class: Type[TResult],
        id_param_name: str = "id",
    ) -> TResult:
        """
        Update a resource by its ID.

        :param resource_id: Resource identifier.
        :param params: Update parameters (Pydantic model or dict).
        :param params_class: Optional Pydantic model class for parameters.
        :param method_class: API method class to use.
        :param result_class: Result model class.
        :param id_param_name: Name of the ID parameter in build method (default: "id").
        :returns: Updated resource instance.
        """
        method = method_class.build(**{id_param_name: resource_id})
        params_dict = normalize_params(params, params_class)
        json_data = method.build_params(**params_dict)
        headers = create_idempotence_headers()
        result = await self._client._send_request(
            method, json=json_data, headers=headers
        )
        return result_class(**result)
