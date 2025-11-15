import abc
import asyncio
import logging
import time
from typing import Any, Dict, Optional, Type, Union

import aiohttp
from aiohttp import BasicAuth, ClientError, ClientSession, ClientTimeout, TCPConnector

from aioyookassa.core.methods.base import APIMethod
from aioyookassa.exceptions import APIError

try:
    from aioyookassa import __version__
except ImportError:
    __version__ = "unknown"


class BaseAPIClient(abc.ABC):
    """Base API Client with connection pooling, timeouts, and resource management."""

    BASE_URL = "https://api.yookassa.ru/v3"
    _DEFAULT_TIMEOUT = ClientTimeout(total=30, connect=5, sock_read=25)
    _DEFAULT_CONNECTOR_CONFIG: Dict[str, Any] = {
        "limit": 100,
        "limit_per_host": 30,
        "ttl_dns_cache": 300,
        "force_close": False,
        "enable_cleanup_closed": True,
    }

    def __init__(
        self,
        api_key: str,
        shop_id: Union[int, str],
        timeout: Optional[ClientTimeout] = None,
        connector: Optional[TCPConnector] = None,
        proxy: Optional[str] = None,
        enable_logging: bool = False,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize Base API Client.

        :param api_key: YooKassa API key
        :param shop_id: YooKassa shop ID
        :param timeout: Custom timeout configuration. Defaults to 30s total, 5s connect, 25s read.
        :param connector: Custom TCP connector. Defaults to optimized connection pooling.
        :param proxy: Proxy URL (e.g., "http://proxy.example.com:8080")
        :param enable_logging: Enable request/response logging
        :param logger: Custom logger instance. If not provided, uses default logger.
        """
        self.api_key = api_key
        self.shop_id = str(shop_id)
        self._session: Optional[ClientSession] = None
        self._proxy = proxy
        self._enable_logging = enable_logging
        self._logger = logger or logging.getLogger(__name__)
        self._timeout = timeout or self._DEFAULT_TIMEOUT
        self._connector = connector
        self._connector_config = (
            None if connector else self._DEFAULT_CONNECTOR_CONFIG.copy()
        )

    def _get_session(self) -> ClientSession:
        """
        Get or create aiohttp ClientSession with optimizations.

        :return: ClientSession with connection pooling and timeouts configured
        """
        if self._session is None or self._session.closed:
            if self._connector is None and self._connector_config:
                loop = self._get_event_loop()
                self._connector = TCPConnector(loop=loop, **self._connector_config)

            self._session = ClientSession(
                connector=self._connector,
                timeout=self._timeout,
                headers={"User-Agent": f"aioyookassa/{__version__}"},
            )
        return self._session

    @staticmethod
    def _get_event_loop() -> Optional[asyncio.AbstractEventLoop]:
        """
        Get running event loop or None if not available.

        :return: Running event loop or None
        """
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return None

    async def close(self) -> None:
        """Close aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _handle_http_error(self, response: Any) -> None:
        """
        Handle HTTP error responses.

        :param response: aiohttp response object
        :raises APIError: Appropriate API error based on response data
        """
        try:
            error_data = await response.json()
        except ValueError:
            # JSON decode error - try to get text response
            try:
                error_text = await response.text()
            except Exception as e:
                raise APIError(
                    f"HTTP {response.status}: Failed to read error response: {str(e)}"
                ) from e
            raise APIError(f"HTTP {response.status}: {error_text}")
        except Exception as e:
            # Other errors (network, etc.)
            raise APIError(
                f"HTTP {response.status}: Failed to parse error response: {str(e)}"
            ) from e

        APIError.detect(
            error_data.get("code", "unknown_error"),
            error_data.get("description", f"HTTP {response.status}"),
            error_details=error_data,
        )

    async def _parse_response(
        self, response: Any, method_instance: APIMethod[Any]
    ) -> dict:
        """
        Parse successful HTTP response.

        :param response: aiohttp response object
        :param method_instance: API Method instance
        :return: Parsed JSON response or empty dict
        :raises APIError: If response parsing fails
        """
        if response.status == 204 or method_instance.http_method == "DELETE":
            try:
                await response.read()
            except (aiohttp.ClientError, asyncio.TimeoutError):
                # Ignore errors when reading empty response body
                pass
            except Exception as e:
                # Log unexpected errors but don't fail
                if self._enable_logging:
                    self._logger.warning(
                        f"Unexpected error reading empty response: {str(e)}"
                    )
            return {}

        try:
            json_result: dict = await response.json()
            return json_result
        except ValueError as e:
            # JSON decode error
            try:
                text = await response.text()
                if not text or text.strip() == "":
                    return {}
                raise APIError(
                    f"Failed to parse JSON response: {str(e)}. Response text: {text[:200]}"
                ) from e
            except Exception as read_error:
                raise APIError(
                    f"Failed to parse JSON response: {str(e)}. "
                    f"Also failed to read response text: {str(read_error)}"
                ) from read_error
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            raise APIError(f"Network error while parsing response: {str(e)}") from e
        except Exception as e:
            raise APIError(f"Unexpected error parsing response: {str(e)}") from e

    async def _send_request(
        self,
        method: Union[Type[APIMethod[Any]], APIMethod[Any]],
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> dict:
        """
        Send request to the API with proper resource management.

        :param method: API Method
        :param json: JSON data
        :param params: Query parameters
        :param headers: Additional headers
        :return: JSON response
        """
        session = self._get_session()
        # Handle both class and instance - normalize to instance once
        if isinstance(method, APIMethod):
            method_instance = method
        else:
            # If it's a class, create a default instance
            method_instance = method()
        request_url = self._get_request_url(method_instance)
        request_headers = {"Content-Type": "application/json"}
        request_headers.update(headers or {})

        auth = (
            None
            if "Authorization" in request_headers
            else BasicAuth(self.shop_id, self.api_key)
        )

        start_time = self._get_current_time() if self._enable_logging else None
        self._log_request(method_instance.http_method, request_url)

        try:
            response = await session.request(
                method_instance.http_method,
                request_url,
                json=self._remove_none_values(json or {}),
                params=self._remove_none_values(params or {}),
                headers=request_headers,
                auth=auth,
                proxy=self._proxy,
                timeout=self._timeout,
            )

            async with response:
                duration = self._calculate_duration(start_time) if start_time else None
                self._log_response(
                    response.status, request_url, duration, method_instance.http_method
                )

                if response.status >= 400:
                    await self._handle_http_error(response)

                return await self._parse_response(response, method_instance)

        except asyncio.TimeoutError:
            self._log_error("timeout", method_instance.http_method, request_url)
            raise APIError(
                f"Request timeout: server did not respond within {self._timeout.total}s"
            )
        except ClientError as e:
            self._log_error("network", method_instance.http_method, request_url, str(e))
            raise APIError(f"Network error: {str(e)}")

    def _get_current_time(self) -> float:
        """
        Get current time using event loop if available, otherwise use time.time().

        :return: Current time as float
        """
        try:
            return asyncio.get_running_loop().time()
        except RuntimeError:
            return time.time()

    def _calculate_duration(self, start_time: float) -> Optional[float]:
        """
        Calculate duration since start_time.

        :param start_time: Start time as float
        :return: Duration in seconds or None
        """
        try:
            return asyncio.get_running_loop().time() - start_time
        except RuntimeError:
            return time.time() - start_time

    def _log_request(self, http_method: str, url: str) -> None:
        """
        Log outgoing HTTP request.

        :param http_method: HTTP method (GET, POST, etc.)
        :param url: Request URL
        """
        if self._enable_logging:
            self._logger.debug(
                f"Sending {http_method} request to {url}",
                extra={"method": http_method, "url": url},
            )

    def _log_response(
        self, status: int, url: str, duration: Optional[float], method: str
    ) -> None:
        """
        Log incoming HTTP response.

        :param status: HTTP status code
        :param url: Request URL
        :param duration: Request duration in seconds
        :param method: HTTP method
        """
        if self._enable_logging:
            duration_msg = f" (duration: {duration:.3f}s)" if duration else ""
            self._logger.debug(
                f"Received {status} response from {url}{duration_msg}",
                extra={
                    "method": method,
                    "url": url,
                    "status": status,
                    "duration": duration,
                },
            )

    def _log_error(
        self, error_type: str, method: str, url: str, details: str = ""
    ) -> None:
        """
        Log request error.

        :param error_type: Type of error (timeout, network, etc.)
        :param method: HTTP method
        :param url: Request URL
        :param details: Additional error details
        """
        if self._enable_logging:
            msg = f"Request {error_type} for {method} {url}"
            if details:
                msg += f": {details}"
            self._logger.error(
                msg,
                extra={"method": method, "url": url},
                exc_info=error_type == "network",
            )

    def _get_request_url(self, method_instance: APIMethod[Any]) -> str:
        """
        Get full URL for API request.

        :param method_instance: API Method instance
        :return: Full request URL
        """
        return f"{self.BASE_URL}{method_instance.path}"

    def _remove_none_values(self, data: dict) -> dict:
        """
        Remove None values recursively from dictionary without mutating original.

        Creates a copy of the dictionary and removes all keys with None values
        recursively, including nested dictionaries and dictionaries in lists.

        :param data: Dictionary to clean
        :return: New dictionary without None values
        """
        result: Dict[str, Any] = {}
        for key, value in data.items():
            if value is None:
                continue
            elif isinstance(value, dict):
                cleaned = self._remove_none_values(value)
                if cleaned:  # Only add non-empty dicts
                    result[key] = cleaned
            elif isinstance(value, list):
                cleaned_list: list = []
                for item in value:
                    if isinstance(item, dict):
                        cleaned_item = self._remove_none_values(item)
                        if cleaned_item:  # Only add non-empty dicts
                            cleaned_list.append(cleaned_item)
                    elif item is not None:
                        cleaned_list.append(item)
                if cleaned_list:  # Only add non-empty lists
                    result[key] = cleaned_list
            else:
                result[key] = value
        return result

    async def __aenter__(self) -> "BaseAPIClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
