Пример работы с Webhooks
=========================

Полный пример настройки и управления webhooks для получения уведомлений о событиях.

**Важно**: Webhooks API требует OAuth-токен для аутентификации. Это API доступно только в рамках Partner API.

Полный код
----------

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.params import CreateWebhookParams
    from aioyookassa.types.enum import WebhookEvent

    async def manage_webhooks():
        """Управление webhooks для получения уведомлений."""
        
        # OAuth токен для Partner API
        oauth_token = "your_oauth_token"
        
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            
            # 1. Создание webhook для уведомлений об успешных платежах
            print("Создание webhook для успешных платежей...")
            params = CreateWebhookParams(
                event=WebhookEvent.PAYMENT_SUCCEEDED,
                url="https://example.com/webhooks/payment-succeeded"
            )
            webhook = await client.webhooks.create_webhook(
                params=params,
                oauth_token=oauth_token
            )
            print(f"✅ Webhook создан: {webhook.id}")
            print(f"📡 Событие: {webhook.event}")
            print(f"🔗 URL: {webhook.url}")
            
            # 2. Создание webhook для отмененных платежей
            print("\nСоздание webhook для отмененных платежей...")
            params = CreateWebhookParams(
                event=WebhookEvent.PAYMENT_CANCELED,
                url="https://example.com/webhooks/payment-canceled"
            )
            webhook = await client.webhooks.create_webhook(
                params=params,
                oauth_token=oauth_token
            )
            print(f"✅ Webhook создан: {webhook.id}")
            
            # 3. Создание webhook для успешных выплат
            print("\nСоздание webhook для успешных выплат...")
            params = CreateWebhookParams(
                event=WebhookEvent.PAYOUT_SUCCEEDED,
                url="https://example.com/webhooks/payout-succeeded"
            )
            webhook = await client.webhooks.create_webhook(
                params=params,
                oauth_token=oauth_token
            )
            print(f"✅ Webhook создан: {webhook.id}")
            
            # 4. Получение списка всех webhooks
            print("\nПолучение списка всех webhooks...")
            webhooks = await client.webhooks.get_webhooks(oauth_token=oauth_token)
            
            if webhooks.list:
                print(f"📊 Всего webhooks: {len(webhooks.list)}")
                for webhook in webhooks.list:
                    print(f"   - {webhook.id}: {webhook.event} -> {webhook.url}")
            else:
                print("   Webhooks не найдены")
            
            # 5. Удаление webhook (пример)
            # print("\nУдаление webhook...")
            # await client.webhooks.delete_webhook(
            #     webhook_id=webhook.id,
            #     oauth_token=oauth_token
            # )
            # print("✅ Webhook удален")

    if __name__ == "__main__":
        asyncio.run(manage_webhooks())

Доступные события
-----------------

- ``WebhookEvent.PAYMENT_WAITING_FOR_CAPTURE`` - платеж ожидает подтверждения
- ``WebhookEvent.PAYMENT_SUCCEEDED`` - платеж успешно выполнен
- ``WebhookEvent.PAYMENT_CANCELED`` - платеж отменен
- ``WebhookEvent.PAYMENT_METHOD_ACTIVE`` - способ оплаты активирован
- ``WebhookEvent.REFUND_SUCCEEDED`` - возврат успешно выполнен
- ``WebhookEvent.PAYOUT_SUCCEEDED`` - выплата успешно выполнена
- ``WebhookEvent.PAYOUT_CANCELED`` - выплата отменена
- ``WebhookEvent.DEAL_CLOSED`` - безопасная сделка закрыта

Обработка webhook уведомлений
------------------------------

Когда YooKassa отправляет уведомление на ваш URL, вы получите POST запрос с данными события:

.. code-block:: python

    from aiohttp import web
    from aioyookassa.types.payment import Payment
    
    async def webhook_handler(request):
        """Обработчик webhook уведомлений."""
        data = await request.json()
        
        # Определяем тип события
        event = data.get('event')
        
        if event == 'payment.succeeded':
            # Обрабатываем успешный платеж
            payment_data = data.get('object')
            payment = Payment(**payment_data)
            
            print(f"✅ Платеж {payment.id} успешно выполнен")
            print(f"💰 Сумма: {payment.amount.value} {payment.amount.currency}")
            
            # Ваша бизнес-логика здесь
            # Например, обновление статуса заказа в БД
            
        elif event == 'payment.canceled':
            # Обрабатываем отмененный платеж
            payment_data = data.get('object')
            payment = Payment(**payment_data)
            
            print(f"❌ Платеж {payment.id} отменен")
            
            # Ваша бизнес-логика здесь
        
        return web.Response(text='OK', status=200)
    
    # Настройка сервера
    app = web.Application()
    app.router.add_post('/webhooks/payment-succeeded', webhook_handler)
    app.router.add_post('/webhooks/payment-canceled', webhook_handler)
    
    web.run_app(app, host='0.0.0.0', port=8080)

Пошаговое объяснение
--------------------

1. **Создание webhook**
   - Указываем событие для отслеживания
   - Указываем URL для получения уведомлений
   - Передаем OAuth токен для аутентификации

2. **Получение списка webhooks**
   - Просматриваем все настроенные webhooks
   - Проверяем их статус и настройки

3. **Удаление webhook**
   - Отписываемся от уведомлений
   - Освобождаем ресурсы

4. **Обработка уведомлений**
   - Настраиваем сервер для приема POST запросов
   - Обрабатываем различные типы событий
   - Выполняем бизнес-логику на основе событий

