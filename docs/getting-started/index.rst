Getting Started
=================

Добро пожаловать в aioyookassa! Этот раздел поможет вам быстро начать работу с библиотекой.

Основы
-------

aioyookassa предоставляет асинхронный интерфейс для работы с API YooKassa. Основные компоненты:

* **YooKassa** — главный клиент для работы с API
* **API модули** — специализированные клиенты для разных операций (payments, refunds, receipts, invoices)
* **Типы данных** — Pydantic модели для валидации данных
* **Исключения** — специальные классы для обработки ошибок

Быстрый старт
--------------

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount, Confirmation
    from aioyookassa.types.enum import ConfirmationType, Currency
    from aioyookassa.types.params import CreatePaymentParams

    async def main():
        # Создание клиента
        client = YooKassa(api_key="your_api_key", shop_id=12345)
        
        # Создание платежа (используем Pydantic модель)
        params = CreatePaymentParams(
            amount=PaymentAmount(value=100.00, currency=Currency.RUB),
            confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com/return"),
            description="Тестовый платеж"
        )
        payment = await client.payments.create_payment(params)
        
        print(f"Payment ID: {payment.id}")
        print(f"Status: {payment.status}")
        print(f"Confirmation URL: {payment.confirmation.url}")
        
        # Закрытие клиента
        await client.close()

    asyncio.run(main())

Контекстный менеджер
--------------------

Рекомендуется использовать контекстный менеджер для автоматического закрытия клиента:

.. code-block:: python

    from aioyookassa.types.payment import PaymentAmount, Confirmation
    from aioyookassa.types.enum import ConfirmationType, Currency
    from aioyookassa.types.params import CreatePaymentParams
    
    async with YooKassa(api_key="your_key", shop_id=12345) as client:
        params = CreatePaymentParams(
            amount=PaymentAmount(value=100.00, currency=Currency.RUB),
            confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com/return")
        )
        payment = await client.payments.create_payment(params)
        # Клиент автоматически закроется

API модули
-----------

Библиотека предоставляет специализированные модули для разных операций:

* **payments** — работа с платежами
* **refunds** — возвраты средств
* **receipts** — фискальные чеки
* **invoices** — счета на оплату
* **payment_methods** — управление способами оплаты

.. toctree::
    :maxdepth: 2
    
    examples
    api-modules
    error-handling
    best-practices