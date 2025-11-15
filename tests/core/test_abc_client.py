"""
Tests for BaseAPIClient.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientError

from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods.base import APIMethod
from aioyookassa.exceptions import APIError


class TestAPIMethod(APIMethod):
    """Test API method for testing."""

    http_method = "GET"
    path = "/test"


class TestBaseAPIClient:
    """Test BaseAPIClient class."""

    def test_base_api_client_initialization(self):
        """Test BaseAPIClient initialization."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        assert client.api_key == "test_api_key"
        assert client.shop_id == "123456"
        assert client._session is None

    def test_base_api_client_initialization_with_string_shop_id(self):
        """Test BaseAPIClient initialization with string shop_id."""
        client = BaseAPIClient(api_key="test_api_key", shop_id="123456")

        assert client.api_key == "test_api_key"
        assert client.shop_id == "123456"

    def test_base_api_client_base_url(self):
        """Test BaseAPIClient base URL."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        assert client.BASE_URL == "https://api.yookassa.ru/v3"

    def test_get_session_creates_new_session(self):
        """Test _get_session creates new session when none exists."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        with patch("aioyookassa.core.abc.client.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value = mock_session

            session = client._get_session()

            assert session == mock_session
            assert client._session == mock_session
            mock_session_class.assert_called_once()

    def test_get_session_reuses_existing_session(self):
        """Test _get_session reuses existing session."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Create a mock session
        mock_session = AsyncMock()
        mock_session.closed = False
        client._session = mock_session

        session = client._get_session()

        assert session == mock_session

    def test_get_session_creates_new_when_closed(self):
        """Test _get_session creates new session when existing is closed."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Create a closed session
        mock_old_session = AsyncMock()
        mock_old_session.closed = True
        client._session = mock_old_session

        with patch("aioyookassa.core.abc.client.ClientSession") as mock_session_class:
            mock_new_session = AsyncMock()
            mock_session_class.return_value = mock_new_session

            session = client._get_session()

            assert session == mock_new_session
            assert client._session == mock_new_session

    @pytest.mark.asyncio
    async def test_close_with_session(self):
        """Test close method with existing session."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Create a mock session
        mock_session = AsyncMock()
        mock_session.closed = False
        client._session = mock_session

        await client.close()

        mock_session.close.assert_called_once()
        assert client._session is None

    @pytest.mark.asyncio
    async def test_close_without_session(self):
        """Test close method without existing session."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Should not raise any errors
        await client.close()
        assert client._session is None

    @pytest.mark.asyncio
    async def test_close_with_closed_session(self):
        """Test close method with already closed session."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Create a closed session
        mock_session = AsyncMock()
        mock_session.closed = True
        client._session = mock_session

        await client.close()

        # Should not call close on already closed session
        mock_session.close.assert_not_called()
        # Session should remain as is since it was already closed
        assert client._session is mock_session

    def test_get_request_url(self):
        """Test _get_request_url method."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        url = client._get_request_url(TestAPIMethod)

        assert url == "https://api.yookassa.ru/v3/test"

    def test_delete_none_with_none_values(self):
        """Test _delete_none method with None values."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        data = {"key1": "value1", "key2": None, "key3": "value3", "key4": None}

        result = client._delete_none(data)

        assert result == {"key1": "value1", "key3": "value3"}

    def test_delete_none_with_nested_dicts(self):
        """Test _delete_none method with nested dictionaries."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        data = {
            "key1": "value1",
            "key2": {
                "nested_key1": "nested_value1",
                "nested_key2": None,
                "nested_key3": "nested_value3",
            },
            "key3": None,
        }

        result = client._delete_none(data)

        expected = {
            "key1": "value1",
            "key2": {"nested_key1": "nested_value1", "nested_key3": "nested_value3"},
        }
        assert result == expected

    def test_delete_none_with_lists(self):
        """Test _delete_none method with lists containing dictionaries."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        data = {
            "key1": "value1",
            "key2": [
                {"item1": "value1", "item2": None},
                {"item3": "value3", "item4": None},
            ],
            "key3": None,
        }

        result = client._delete_none(data)

        expected = {
            "key1": "value1",
            "key2": [{"item1": "value1"}, {"item3": "value3"}],
        }
        assert result == expected

    def test_delete_none_with_empty_dict(self):
        """Test _delete_none method with empty dictionary."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        data = {}
        result = client._delete_none(data)

        assert result == {}

    def test_delete_none_with_no_none_values(self):
        """Test _delete_none method with no None values."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        data = {"key1": "value1", "key2": "value2", "key3": "value3"}

        result = client._delete_none(data)

        assert result == data

    @pytest.mark.asyncio
    async def test_send_request_success(self):
        """Test _send_request method with successful response."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Mock session and response
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})
        mock_session.request.return_value = mock_response

        with patch.object(client, "_get_session", return_value=mock_session):
            result = await client._send_request(TestAPIMethod)

            assert result == {"success": True}
            mock_session.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_request_with_json_data(self):
        """Test _send_request method with JSON data."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Mock session and response
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})
        mock_session.request.return_value = mock_response

        with patch.object(client, "_get_session", return_value=mock_session):
            json_data = {"key": "value"}
            headers = {"Content-Type": "application/json"}

            result = await client._send_request(
                TestAPIMethod, json=json_data, headers=headers
            )

            assert result == {"success": True}

            # Check that request was called with correct parameters
            call_args = mock_session.request.call_args
            assert call_args[1]["json"] == json_data
            assert call_args[1]["headers"]["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    async def test_send_request_with_params(self):
        """Test _send_request method with query parameters."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Mock session and response
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})
        mock_session.request.return_value = mock_response

        with patch.object(client, "_get_session", return_value=mock_session):
            params = {"param1": "value1", "param2": "value2"}

            result = await client._send_request(TestAPIMethod, params=params)

            assert result == {"success": True}

            # Check that request was called with correct parameters
            call_args = mock_session.request.call_args
            assert call_args[1]["params"] == params

    @pytest.mark.asyncio
    async def test_send_request_http_error_with_json(self):
        """Test _send_request method with HTTP error and JSON response."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Mock session and response
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 400
        mock_response.json = AsyncMock(
            return_value={"code": "invalid_request", "description": "Invalid request"}
        )
        mock_session.request.return_value = mock_response

        with patch.object(client, "_get_session", return_value=mock_session):
            with pytest.raises(APIError) as exc_info:
                await client._send_request(TestAPIMethod)

            assert "Invalid request" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_send_request_http_error_with_text(self):
        """Test _send_request method with HTTP error and text response."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Mock session and response
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 400
        mock_response.json.side_effect = Exception("Not JSON")
        mock_response.text = AsyncMock(return_value="Bad Request")
        mock_session.request.return_value = mock_response

        with patch.object(client, "_get_session", return_value=mock_session):
            with pytest.raises(APIError) as exc_info:
                await client._send_request(TestAPIMethod)

            assert "HTTP 400: Bad Request" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_send_request_network_error(self):
        """Test _send_request method with network error."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Mock session
        mock_session = AsyncMock()
        mock_session.request.side_effect = ClientError("Network error")

        with patch.object(client, "_get_session", return_value=mock_session):
            with pytest.raises(APIError) as exc_info:
                await client._send_request(TestAPIMethod)

            assert "Network error: Network error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_send_request_json_parse_error(self):
        """Test _send_request method with JSON parse error."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        # Mock session and response
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.side_effect = Exception("JSON parse error")
        # Configure text() to return non-empty string to avoid empty response handling
        mock_response.text = AsyncMock(return_value="some text")
        mock_session.request.return_value = mock_response

        with patch.object(client, "_get_session", return_value=mock_session):
            with pytest.raises(APIError) as exc_info:
                await client._send_request(TestAPIMethod)

            assert "Failed to parse JSON response: JSON parse error" in str(
                exc_info.value
            )

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test BaseAPIClient as context manager."""
        client = BaseAPIClient(api_key="test_api_key", shop_id=123456)

        async with client as ctx:
            assert ctx is client
            assert ctx.api_key == "test_api_key"
            assert ctx.shop_id == "123456"
