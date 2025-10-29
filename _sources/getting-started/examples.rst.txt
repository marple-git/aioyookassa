Примеры использования
=====================

В этом разделе представлены практические примеры использования aioyookassa для различных задач.

💳 Платежи
----------

Создание платежа
~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount, Confirmation

    async def create_payment():
        async with YooKassa('your_api_key', 12345) as client:
            confirmation = Confirmation(
                type='redirect', 
                return_url='https://example.com/return'
            )
            payment = await client.payments.create_payment(
                amount=PaymentAmount(value=100.00, currency='RUB'),
                description='Тестовый платеж',
                confirmation=confirmation
            )
            print(f"Payment ID: {payment.id}")
            print(f"Confirmation URL: {payment.confirmation.confirmation_url}")

    asyncio.run(create_payment())

Получение списка платежей
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from datetime import datetime
    from aioyookassa import YooKassa
    from aioyookassa.types.enum import PaymentStatus

    async def get_payments():
        async with YooKassa('your_api_key', 12345) as client:
            # Получение всех платежей
            payments = await client.payments.get_payments()
            print(f"Всего платежей: {len(payments.list)}")
            
            # Получение платежей с фильтрами
            filtered_payments = await client.payments.get_payments(
                created_at=datetime(2023, 1, 1, 12, 0, 0),
                status=PaymentStatus.SUCCEEDED,
                limit=10
            )
            
            for payment in filtered_payments.list:
                print(f"Payment: {payment.id}, Amount: {payment.amount.value} {payment.amount.currency}")

    asyncio.run(get_payments())

Получение конкретного платежа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def get_payment():
        async with YooKassa('your_api_key', 12345) as client:
            payment = await client.payments.get_payment('PAYMENT_ID')
            print(f"Payment ID: {payment.id}")
            print(f"Status: {payment.status}")
            print(f"Amount: {payment.amount.value} {payment.amount.currency}")
            print(f"Description: {payment.description}")

    asyncio.run(get_payment())

Подтверждение платежа
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def capture_payment():
        async with YooKassa('your_api_key', 12345) as client:
            payment = await client.payments.capture_payment('payment_id')
            print(f"Payment captured: {payment.id}")
            print(f"Status: {payment.status}")

    asyncio.run(capture_payment())

Отмена платежа
~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def cancel_payment():
        async with YooKassa('your_api_key', 12345) as client:
            payment = await client.payments.cancel_payment('payment_id')
            print(f"Payment cancelled: {payment.id}")
            print(f"Status: {payment.status}")

    asyncio.run(cancel_payment())

💰 Возвраты
-----------

Создание возврата
~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount

    async def create_refund():
        async with YooKassa('your_api_key', 12345) as client:
            refund = await client.refunds.create_refund(
                payment_id='payment_id',
                amount=PaymentAmount(value=50.00, currency='RUB'),
                description='Частичный возврат'
            )
            print(f"Refund ID: {refund.id}")
            print(f"Status: {refund.status}")

    asyncio.run(create_refund())

Получение информации о возврате
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def get_refund():
        async with YooKassa('your_api_key', 12345) as client:
            refund = await client.refunds.get_refund('refund_id')
            print(f"Refund ID: {refund.id}")
            print(f"Amount: {refund.amount.value} {refund.amount.currency}")
            print(f"Status: {refund.status}")

    asyncio.run(get_refund())

🧾 Чеки
-------

Регистрация чека
~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount

    async def create_receipt():
        async with YooKassa('your_api_key', 12345) as client:
            receipt = await client.receipts.create_receipt(
                payment_id='payment_id',
                items=[
                    {
                        "description": "Товар",
                        "quantity": 1,
                        "amount": PaymentAmount(value=1000.00, currency='RUB'),
                        "vat_code": 1
                    }
                ],
                tax_system_code=1
            )
            print(f"Receipt ID: {receipt.id}")
            print(f"Status: {receipt.status}")

    asyncio.run(create_receipt())

📄 Счета
--------

Создание счета
~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount

    async def create_invoice():
        async with YooKassa('your_api_key', 12345) as client:
            invoice = await client.invoices.create_invoice(
                amount=PaymentAmount(value=2000.00, currency='RUB'),
                description='Счет на оплату'
            )
            print(f"Invoice ID: {invoice.id}")
            print(f"Status: {invoice.status}")

    asyncio.run(create_invoice())

🔄 Обработка ошибок
-------------------

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.exceptions import APIError, NotFound, InvalidCredentials

    async def handle_errors():
        async with YooKassa('your_api_key', 12345) as client:
            try:
                payment = await client.payments.get_payment('invalid_id')
            except NotFound:
                print("Платеж не найден")
            except InvalidCredentials:
                print("Неверные учетные данные")
            except APIError as e:
                print(f"Ошибка API: {e}")

    asyncio.run(handle_errors())
