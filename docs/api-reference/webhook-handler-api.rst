Webhook Handler API
====================

API для обработки входящих webhook-уведомлений от YooKassa.

Библиотека предоставляет два подхода к обработке webhook-уведомлений:

1. **WebhookHandler** — базовый обработчик для интеграции с любым веб-фреймворком
2. **WebhookServer** — готовый сервер на aiohttp для быстрого старта

WebhookHandler
--------------

Базовый класс для обработки webhook-уведомлений. Работает с любым веб-фреймворком.

.. autoclass:: aioyookassa.core.webhook_handler.WebhookHandler
   :members:
   :show-inheritance:

Методы
~~~~~~

parse_notification
~~~~~~~~~~~~~~~~~~

Парсит сырые данные webhook-уведомления в типизированную модель.

.. code-block:: python

    from aioyookassa.core.webhook_handler import WebhookHandler
    
    handler = WebhookHandler()
    data = await request.json()
    notification = handler.parse_notification(data)
    
    print(f"Event: {notification.event}")
    print(f"Type: {notification.type}")

handle_notification
~~~~~~~~~~~~~~~~~~~

Обрабатывает уведомление и возвращает типизированный объект события.

.. code-block:: python

    notification = handler.parse_notification(data)
    event_object = await handler.handle_notification(notification)
    
    # event_object будет типизированным объектом:
    # - Payment для payment.* событий
    # - Refund для refund.* событий
    # - Payout для payout.* событий
    # - Deal для deal.closed
    # - PaymentMethod для payment_method.active

Регистрация callbacks
~~~~~~~~~~~~~~~~~~~~~~

Декоратор для регистрации обработчиков событий.

.. code-block:: python

    from aioyookassa.types.enum import WebhookEvent
    from aioyookassa.types.payment import Payment
    
    @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
    async def on_payment_succeeded(payment: Payment):
        print(f"Payment {payment.id} succeeded")
        # Ваша бизнес-логика

Регистрация для нескольких событий:

.. code-block:: python

    @handler.register_callback([
        WebhookEvent.PAYMENT_SUCCEEDED,
        WebhookEvent.PAYMENT_CANCELED
    ])
    async def on_payment_status_change(payment: Payment):
        print(f"Payment {payment.id} status changed")

Регистрация с паттерном (wildcard):

.. code-block:: python

    @handler.register_callback("payment.*")
    async def handle_all_payments(payment: Payment):
        print(f"Payment event: {payment.id}")

add_callback
~~~~~~~~~~~~

Обычный метод для регистрации callbacks без декоратора.

.. code-block:: python

    async def my_handler(payment: Payment):
        print(f"Payment {payment.id} processed")
    
    handler.add_callback(WebhookEvent.PAYMENT_SUCCEEDED, my_handler)

WebhookIPValidator
------------------

Валидатор IP-адресов для проверки, что запросы приходят от YooKassa.

.. autoclass:: aioyookassa.core.webhook_validator.WebhookIPValidator
   :members:
   :show-inheritance:

Использование
~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.core.webhook_validator import WebhookIPValidator
    
    validator = WebhookIPValidator()
    
    # Проверка IP
    if validator.is_allowed("185.71.76.1"):
        print("IP is allowed")
    
    # Кастомный список IP (для тестирования)
    custom_validator = WebhookIPValidator(
        allowed_ips=["127.0.0.1", "192.168.1.0/24"]
    )

WebhookServer
-------------

Готовый сервер на aiohttp для обработки webhook-уведомлений.

.. autoclass:: aioyookassa.contrib.webhook_server.WebhookServer
   :members:
   :show-inheritance:

Использование
~~~~~~~~~~~~

Быстрый старт:

.. code-block:: python

    from aioyookassa.contrib.webhook_server import WebhookServer
    from aioyookassa.core.webhook_handler import WebhookHandler
    from aioyookassa.types.enum import WebhookEvent
    
    handler = WebhookHandler()
    
    @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
    async def on_payment(payment):
        print(f"Payment {payment.id} succeeded")
    
    server = WebhookServer(handler=handler)
    server.run(host="0.0.0.0", port=8080)

Создание приложения для интеграции:

.. code-block:: python

    app = server.create_app()
    # Можно добавить дополнительные роуты, middleware и т.д.

Примеры использования
---------------------

Интеграция с aiohttp
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aiohttp import web
    from aioyookassa.core.webhook_handler import WebhookHandler
    from aioyookassa.types.enum import WebhookEvent
    
    handler = WebhookHandler()
    
    @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
    async def on_payment_succeeded(payment):
        await process_payment(payment)
    
    async def webhook_endpoint(request):
        # Валидация IP
        if not handler.validator.is_allowed(request.remote):
            raise web.HTTPForbidden()
        
        # Обработка
        data = await request.json()
        notification = handler.parse_notification(data)
        await handler.handle_notification(notification)
        
        return web.Response(status=200)
    
    app = web.Application()
    app.router.add_post("/webhook", webhook_endpoint)
    web.run_app(app)

Интеграция с FastAPI
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from fastapi import FastAPI, Request, HTTPException
    from aioyookassa.core.webhook_handler import WebhookHandler
    from aioyookassa.types.enum import WebhookEvent
    
    handler = WebhookHandler()
    app = FastAPI()
    
    @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
    async def on_payment_succeeded(payment):
        await process_payment(payment)
    
    @app.post("/webhook")
    async def webhook_endpoint(request: Request):
        # Валидация IP
        if not handler.validator.is_allowed(request.client.host):
            raise HTTPException(status_code=403)
        
        # Обработка
        data = await request.json()
        notification = handler.parse_notification(data)
        await handler.handle_notification(notification)
        
        return {"status": "ok"}

Валидация IP
------------

По умолчанию валидация IP включена и использует официальные IP-адреса YooKassa:

- 185.71.76.0/27
- 185.71.77.0/27
- 77.75.153.0/25
- 77.75.156.11
- 77.75.156.35
- 77.75.154.128/25
- 2a02:5180::/32

Для отключения валидации (только для разработки!):

.. code-block:: python

    from aioyookassa.core.webhook_validator import WebhookIPValidator
    
    # Разрешить все IP (не рекомендуется для production)
    validator = WebhookIPValidator(allowed_ips=["0.0.0.0/0"])
    handler = WebhookHandler(validator=validator)

Поддерживаемые события
----------------------

- ``payment.waiting_for_capture`` — платеж ожидает подтверждения
- ``payment.succeeded`` — платеж успешно выполнен
- ``payment.canceled`` — платеж отменен
- ``payment_method.active`` — способ оплаты активирован
- ``refund.succeeded`` — возврат успешно выполнен
- ``payout.succeeded`` — выплата успешно выполнена
- ``payout.canceled`` — выплата отменена
- ``deal.closed`` — безопасная сделка закрыта

Исключения
----------

.. automodule:: aioyookassa.exceptions.webhooks
   :members:

