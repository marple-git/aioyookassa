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
    from aioyookassa.types.enum import ConfirmationType, Currency
    from aioyookassa.types.params import CreatePaymentParams

    async def create_payment():
        async with YooKassa('your_api_key', 12345) as client:
            confirmation = Confirmation(
                type=ConfirmationType.REDIRECT, 
                return_url='https://example.com/return'
            )
            params = CreatePaymentParams(
                amount=PaymentAmount(value=100.00, currency=Currency.RUB),
                description='Тестовый платеж',
                confirmation=confirmation
            )
            payment = await client.payments.create_payment(params)
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
    from aioyookassa.types.params import GetPaymentsParams

    async def get_payments():
        async with YooKassa('your_api_key', 12345) as client:
            # Получение всех платежей
            payments = await client.payments.get_payments()
            print(f"Всего платежей: {len(payments.list)}")
            
            # Получение платежей с фильтрами (используем Pydantic модель)
            params = GetPaymentsParams(
                created_at=datetime(2023, 1, 1, 12, 0, 0),
                status=PaymentStatus.SUCCEEDED,
                limit=10
            )
            filtered_payments = await client.payments.get_payments(params)
            
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
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreateRefundParams

    async def create_refund():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreateRefundParams(
                payment_id='payment_id',
                amount=PaymentAmount(value=50.00, currency=Currency.RUB),
                description='Частичный возврат'
            )
            refund = await client.refunds.create_refund(params)
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
    from aioyookassa.types.payment import PaymentAmount, Customer, Settlement
    from aioyookassa.types.enum import Currency, ReceiptType
    from aioyookassa.types.params import CreateReceiptParams
    from aioyookassa.types.receipt_registration import ReceiptRegistrationItem

    async def create_receipt():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreateReceiptParams(
                type=ReceiptType.PAYMENT,
                payment_id='payment_id',
                customer=Customer(email="customer@example.com"),
                items=[
                    ReceiptRegistrationItem(
                        description="Товар",
                        quantity=1,
                        amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
                        vat_code=1,
                        payment_subject="commodity",
                        payment_mode="full_payment"
                    )
                ],
                settlements=[
                    Settlement(type="prepayment", amount=PaymentAmount(value=1000.00, currency=Currency.RUB))
                ],
                tax_system_code=1
            )
            receipt = await client.receipts.create_receipt(params)
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
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreateInvoiceParams

    async def create_invoice():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreateInvoiceParams(
                amount=PaymentAmount(value=2000.00, currency=Currency.RUB),
                description='Счет на оплату'
            )
            invoice = await client.invoices.create_invoice(params)
            print(f"Invoice ID: {invoice.id}")
            print(f"Status: {invoice.status}")

    asyncio.run(create_invoice())

⚙️ Настройки магазина
---------------------

Получение информации о настройках магазина или шлюза
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def get_settings():
        async with YooKassa('your_api_key', 12345) as client:
            # Получение настроек текущего магазина
            settings = await client.get_me()
            
            print(f"Account ID: {settings.account_id}")
            print(f"Status: {settings.status}")
            print(f"Test mode: {settings.test}")
            
            # Проверка настроек фискализации
            if settings.fiscalization:
                print(f"Fiscalization enabled: {settings.fiscalization.enabled}")
                print(f"Provider: {settings.fiscalization.provider}")
            
            # Список доступных способов оплаты
            if settings.payment_methods:
                print(f"Available payment methods: {', '.join(settings.payment_methods)}")
            
            # ИНН магазина
            if settings.itn:
                print(f"ITN: {settings.itn}")
            
            # Для Сплитования платежей - получение настроек магазина продавца
            if settings.payout_methods:
                print(f"Payout methods: {', '.join(settings.payout_methods)}")
            
            # Баланс шлюза (для выплат)
            if settings.payout_balance:
                print(f"Payout balance: {settings.payout_balance.value} {settings.payout_balance.currency}")

    asyncio.run(get_settings())

Получение настроек для Сплитования платежей
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def get_seller_settings():
        async with YooKassa('your_api_key', 12345) as client:
            # Получение настроек магазина продавца
            seller_settings = await client.get_me(on_behalf_of="seller_shop_id")
            
            print(f"Seller Account ID: {seller_settings.account_id}")
            print(f"Seller Status: {seller_settings.status}")
            
            # Проверка доступных способов оплаты для продавца
            if seller_settings.payment_methods:
                print(f"Seller payment methods: {', '.join(seller_settings.payment_methods)}")

    asyncio.run(get_seller_settings())

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
