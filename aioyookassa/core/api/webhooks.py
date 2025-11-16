from typing import Optional, Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods.webhooks import CreateWebhook, DeleteWebhook, GetWebhooks
from aioyookassa.types.params import CreateWebhookParams
from aioyookassa.types.webhooks import Webhook, WebhooksList


class WebhooksAPI(BaseAPI[CreateWebhookParams, Webhook]):
    """
    YooKassa webhooks API client.

    Provides methods for creating, retrieving, and deleting webhooks.
    Webhooks API requires OAuth token for authentication.
    """

    async def create_webhook(
        self,
        params: CreateWebhookParams,
        oauth_token: str,
    ) -> Webhook:
        """
        Create a new webhook in YooKassa.

        :param params: Webhook creation parameters (CreateWebhookParams).
        :type params: CreateWebhookParams
        :param oauth_token: OAuth token for authentication.
        :type oauth_token: str
        :returns: Webhook object.
        :rtype: Webhook
        :seealso: https://yookassa.ru/developers/api#create_webhook
        """
        from aioyookassa.core.utils import normalize_params

        params_dict = normalize_params(params, CreateWebhookParams)
        json_data = CreateWebhook.build_params(**params_dict)
        headers = {
            "Authorization": f"Bearer {oauth_token}",
        }
        from aioyookassa.core.utils import create_idempotence_headers

        headers.update(create_idempotence_headers())
        result = await self._client._send_request(
            CreateWebhook, json=json_data, headers=headers
        )
        return Webhook(**result)

    async def get_webhooks(
        self,
        oauth_token: str,
    ) -> WebhooksList:
        """
        Retrieve a list of webhooks for the OAuth token.

        :param oauth_token: OAuth token for authentication.
        :type oauth_token: str
        :returns: WebhooksList object.
        :rtype: WebhooksList
        :seealso: https://yookassa.ru/developers/api#list_webhooks
        """
        headers = {
            "Authorization": f"Bearer {oauth_token}",
        }
        result = await self._client._send_request(GetWebhooks, headers=headers)
        return WebhooksList(**result)

    async def delete_webhook(
        self,
        webhook_id: str,
        oauth_token: str,
    ) -> None:
        """
        Delete a webhook by its ID.

        :param webhook_id: Webhook identifier.
        :type webhook_id: str
        :param oauth_token: OAuth token for authentication.
        :type oauth_token: str
        :seealso: https://yookassa.ru/developers/api#delete_webhook
        """
        method = DeleteWebhook.build(webhook_id=webhook_id)
        headers = {
            "Authorization": f"Bearer {oauth_token}",
        }
        # DELETE returns empty body (204 No Content), _send_request handles it
        await self._client._send_request(method, headers=headers)
