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

    async def main():
        # Создание клиента
        client = YooKassa(api_key="your_api_key", shop_id=12345)
        
        # Создание платежа
        payment = await client.payments.create_payment(
            amount=PaymentAmount(value=100.00, currency="RUB"),
            confirmation=Confirmation(type="redirect", return_url="https://example.com/return"),
            description="Тестовый платеж"
        )
        
        print(f"Payment ID: {payment.id}")
        print(f"Status: {payment.status}")
        
        # Закрытие клиента
        await client.close()

    asyncio.run(main())

Контекстный менеджер
--------------------

Рекомендуется использовать контекстный менеджер для автоматического закрытия клиента:

.. code-block:: python

    async with YooKassa(api_key="your_key", shop_id=12345) as client:
        payment = await client.payments.create_payment(
            amount=PaymentAmount(value=100.00, currency="RUB"),
            confirmation=Confirmation(type="redirect", return_url="https://example.com/return")
        )
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