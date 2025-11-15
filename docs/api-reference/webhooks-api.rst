Webhooks API
============

API для работы с webhooks (уведомлениями о событиях).

**Важно**: Webhooks API требует OAuth-токен для аутентификации. Это API доступно только в рамках Partner API.

.. autoclass:: aioyookassa.core.api.webhooks.WebhooksAPI
   :members:
   :show-inheritance:

Методы
------

create_webhook
~~~~~~~~~~~~~~

Создание нового webhook для подписки на события.

.. code-block:: python

    from aioyookassa.types.params import CreateWebhookParams
    from aioyookassa.types.enum import WebhookEvent
    
    params = CreateWebhookParams(
        event=WebhookEvent.PAYMENT_SUCCEEDED,
        url="https://example.com/webhook"
    )
    webhook = await client.webhooks.create_webhook(
        params=params,
        oauth_token="your_oauth_token"
    )
    
    # Доступные события:
    # - WebhookEvent.PAYMENT_WAITING_FOR_CAPTURE
    # - WebhookEvent.PAYMENT_SUCCEEDED
    # - WebhookEvent.PAYMENT_CANCELED
    # - WebhookEvent.PAYMENT_METHOD_ACTIVE
    # - WebhookEvent.REFUND_SUCCEEDED
    # - WebhookEvent.PAYOUT_SUCCEEDED
    # - WebhookEvent.PAYOUT_CANCELED
    # - WebhookEvent.DEAL_CLOSED

get_webhooks
~~~~~~~~~~~~

Получение списка всех webhooks для OAuth-токена.

.. code-block:: python

    webhooks = await client.webhooks.get_webhooks(oauth_token="your_oauth_token")
    
    if webhooks.list:
        for webhook in webhooks.list:
            print(f"Webhook {webhook.id}: {webhook.event} -> {webhook.url}")

delete_webhook
~~~~~~~~~~~~~~

Удаление webhook.

.. code-block:: python

    await client.webhooks.delete_webhook(
        webhook_id="webhook_id",
        oauth_token="your_oauth_token"
    )

