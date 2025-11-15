..

aioyookassa Documentation
=========================

**Асинхронная Python библиотека для работы с API YooKassa**

`aioyookassa` — это современная асинхронная библиотека для интеграции с платежным сервисом YooKassa. Библиотека предоставляет полную поддержку всех API доменов YooKassa, включая платежи, возвраты, чеки, счета, выплаты, безопасные сделки, webhooks и многое другое.

.. image:: https://pepy.tech/badge/aioyookassa
   :target: https://pepy.tech/project/aioyookassa
   :alt: Downloads

.. image:: https://pepy.tech/badge/aioyookassa/month
   :target: https://pepy.tech/project/aioyookassa
   :alt: Downloads per month

.. image:: https://api.codiga.io/project/34833/score/svg
   :target: https://api.codiga.io/project/34833/score/svg
   :alt: Code Quality Score

.. image:: https://api.codiga.io/project/34833/status/svg
   :target: https://api.codiga.io/project/34833/status/svg
   :alt: Code Grade

✨ **Особенности**
------------------

* 🚀 **Асинхронность** — полная поддержка `asyncio` для высокопроизводительных приложений
* 🛡️ **Типизация** — полная поддержка типов с использованием Pydantic моделей
* 🔧 **Простота** — интуитивно понятный API для быстрой интеграции
* 📚 **Документация** — подробная документация с примерами использования
* 🧪 **Тестирование** — 95% покрытие кода тестами
* ⚡ **Производительность** — оптимизированная работа с HTTP запросами
* 🎯 **Полная поддержка API** — реализованы все домены YooKassa API

🚀 **Быстрый старт**
-------------------

Установка
~~~~~~~~~

.. code-block:: bash

    pip install aioyookassa>=2.0.0

Базовое использование
~~~~~~~~~~~~~~~~~~~~~

.. note::

   В версии 2.1.0 `PaymentAmount` переименован в `Money` для лучшей семантики.
   `PaymentAmount` все еще доступен как alias для обратной совместимости.

.. code-block:: python

    import asyncio
    from datetime import datetime
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money, Confirmation
    from aioyookassa.types.enum import PaymentStatus, ConfirmationType, Currency
    from aioyookassa.types.params import CreatePaymentParams, GetPaymentsParams

    async def main():
        # Инициализация клиента
        client = YooKassa(api_key="your_api_key", shop_id=12345)

        # Создание платежа (используем Pydantic модель)
        params = CreatePaymentParams(
            amount=Money(value=100.00, currency=Currency.RUB),
            confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com/return"),
            description="Тестовый платеж"
        )
        payment = await client.payments.create_payment(params)

        print(f"Payment created: {payment.id}")
        print(f"Confirmation URL: {payment.confirmation.url}")

        # Получение информации о платеже
        payment_info = await client.payments.get_payment(payment.id)
        print(f"Payment status: {payment_info.status}")

        # Получение списка платежей за сегодня (используем Pydantic модель)
        today = datetime.now()
        params = GetPaymentsParams(
            created_at=today,
            status=PaymentStatus.SUCCEEDED
        )
        payments = await client.payments.get_payments(params)
        print(f"Found {len(payments.list)} successful payments today")

        # Закрытие клиента
        await client.close()

    # Запуск
    asyncio.run(main())

🎯 **Поддерживаемые API домены**
---------------------------------

Библиотека поддерживает **все API домены YooKassa**:

* 💳 **Платежи (Payments)** — создание, подтверждение, отмена платежей
* 💰 **Возвраты (Refunds)** — полные и частичные возвраты
* 🧾 **Чеки (Receipts)** — регистрация фискальных чеков
* 📄 **Счета (Invoices)** — создание и управление счетами
* 💳 **Способы оплаты (Payment Methods)** — управление сохраненными способами оплаты
* 💸 **Выплаты (Payouts)** — выплаты на карты, через СБП, на кошельки ЮMoney
* 👤 **Самозанятые (Self-Employed)** — работа с самозанятыми получателями
* 🏦 **Участники СБП (SBP Banks)** — получение списка банков СБП
* 🔐 **Персональные данные (Personal Data)** — управление персональными данными получателей
* 🤝 **Безопасные сделки (Deals)** — создание и управление безопасными сделками
* 🔔 **Webhooks** — подписка на события, управление уведомлениями и обработка входящих webhook-уведомлений

Обработка webhook-уведомлений
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Библиотека предоставляет удобные инструменты для обработки входящих webhook-уведомлений:

**Готовый сервер (быстрый старт):**

.. code-block:: python

    from aioyookassa.contrib.webhook_server import WebhookServer
    from aioyookassa.core.webhook_handler import WebhookHandler
    from aioyookassa.types.enum import WebhookEvent
    from aioyookassa.types.payment import Payment

    handler = WebhookHandler()

    @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
    async def on_payment_succeeded(payment: Payment):
        print(f"✅ Платеж {payment.id} успешно выполнен")
        # Ваша бизнес-логика

    server = WebhookServer(handler=handler)
    server.run(host="0.0.0.0", port=8080)

**Интеграция с существующим приложением:**

.. code-block:: python

    from aiohttp import web
    from aioyookassa.core.webhook_handler import WebhookHandler
    from aioyookassa.types.enum import WebhookEvent
    from aioyookassa.types.payment import Payment

    handler = WebhookHandler()

    @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
    async def on_payment_succeeded(payment: Payment):
        await process_payment(payment)

    async def webhook_endpoint(request):
        # Валидация IP (рекомендуется)
        if not handler.validator.is_allowed(request.remote):
            raise web.HTTPForbidden()

        # Обработка уведомления
        data = await request.json()
        notification = handler.parse_notification(data)
        await handler.handle_notification(notification)

        return web.Response(status=200)

    app = web.Application()
    app.router.add_post("/webhook", webhook_endpoint)
    web.run_app(app)

Подробнее об обработке webhook-уведомлений см. в разделе :doc:`api-reference/webhook-handler-api`.

📖 **Содержание**
----------------

.. toctree::
   :maxdepth: 2
   
   installation
   getting-started/index
   api-reference/index
   types/index
   examples/index
   changelog
   contributing

⚠️ **Breaking Changes в версии 2.0.0**
---------------------------------------

**Версия 2.0.0 содержит breaking changes:**

* **Удалены дублирующиеся типы:**
  * `RefundCancellationDetails` → используйте `CancellationDetails`
  * `RefundSettlement` → используйте `Settlement`
  * `ReceiptSettlement` → используйте `Settlement`

**Миграция:**

.. code-block:: python

    # До версии 2.0.0
    from aioyookassa.types import RefundCancellationDetails, RefundSettlement, ReceiptSettlement

    # Версия 2.0.0+
    from aioyookassa.types import CancellationDetails, Settlement

Подробности в :doc:`changelog`.

🔗 **Ссылки**
-------------

* `GitHub Repository <https://github.com/masasibata/aioyookassa>`_
* `PyPI Package <https://pypi.org/project/aioyookassa/>`_
* `YooKassa API Documentation <https://yookassa.ru/developers/api>`_

💝 **Поддержка проекта**
-----------------------

Если библиотека оказалась полезной, вы можете поддержать проект:

* `Tribute <https://t.me/tribute/app?startapp=dzqR>`_ — поддержка через Telegram
* `Telegram разработчика <https://t.me/masaasibaata>`_ — связаться с разработчиком

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
