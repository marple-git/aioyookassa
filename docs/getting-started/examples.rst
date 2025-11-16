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
            print(f"Confirmation URL: {payment.confirmation.url}")

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
    from aioyookassa.types.enum import Currency, ReceiptType, PaymentSubject, PaymentMode
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
                        payment_subject=PaymentSubject.COMMODITY,
                        payment_mode=PaymentMode.FULL_PAYMENT
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

💸 Выплаты
----------

Создание выплаты на банковскую карту
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import (
        CreatePayoutParams,
        BankCardPayoutDestinationData,
        BankCardPayoutCardData
    )

    async def create_payout():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreatePayoutParams(
                amount=Money(value=5000.00, currency=Currency.RUB),
                payout_destination_data=BankCardPayoutDestinationData(
                    card=BankCardPayoutCardData(number="5555555555554477")
                ),
                description="Выплата по договору"
            )
            payout = await client.payouts.create_payout(params)
            print(f"Payout ID: {payout.id}")
            print(f"Status: {payout.status}")

    asyncio.run(create_payout())

Создание выплаты через СБП
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import (
        CreatePayoutParams,
        SbpPayoutDestinationData
    )

    async def create_sbp_payout():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreatePayoutParams(
                amount=Money(value=3000.00, currency=Currency.RUB),
                payout_destination_data=SbpPayoutDestinationData(
                    bank_id="100000000111",
                    phone="79001234567"
                ),
                description="Выплата через СБП"
            )
            payout = await client.payouts.create_payout(params)
            print(f"Payout ID: {payout.id}")

    asyncio.run(create_sbp_payout())

🤝 Безопасные сделки
--------------------

Создание безопасной сделки
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.enum import FeeMoment
    from aioyookassa.types.params import CreateDealParams

    async def create_deal():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreateDealParams(
                fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
                description="Безопасная сделка"
            )
            deal = await client.deals.create_deal(params)
            print(f"Deal ID: {deal.id}")
            print(f"Status: {deal.status}")

    asyncio.run(create_deal())

Создание платежа с привязкой к сделке
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money, Confirmation
    from aioyookassa.types.enum import Currency, ConfirmationType
    from aioyookassa.types.params import CreatePaymentParams

    async def create_payment_with_deal():
        async with YooKassa('your_api_key', 12345) as client:
            # Сначала создаем сделку
            deal = await client.deals.create_deal(
                CreateDealParams(
                    fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
                    description="Сделка для платежа"
                )
            )
            
            # Создаем платеж с привязкой к сделке
            params = CreatePaymentParams(
                amount=Money(value=10000.00, currency=Currency.RUB),
                confirmation=Confirmation(
                    type=ConfirmationType.REDIRECT,
                    return_url="https://example.com/return"
                ),
                description="Платеж по сделке",
                deal=deal.id
            )
            payment = await client.payments.create_payment(params)
            print(f"Payment ID: {payment.id}")
            print(f"Deal ID: {deal.id}")

    asyncio.run(create_payment_with_deal())

👤 Самозанятые
--------------

Создание самозанятого
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.params import (
        CreateSelfEmployedParams,
        SelfEmployedConfirmationData
    )

    async def create_self_employed():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreateSelfEmployedParams(
                itn="123456789012",
                confirmation=SelfEmployedConfirmationData(
                    type="redirect",
                    confirmation_url="https://example.com/confirm"
                )
            )
            self_employed = await client.self_employed.create_self_employed(params)
            print(f"Self-Employed ID: {self_employed.id}")
            print(f"Status: {self_employed.status}")

    asyncio.run(create_self_employed())

🏦 Участники СБП
---------------

Получение списка банков СБП
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def get_sbp_banks():
        async with YooKassa('your_api_key', 12345) as client:
            sbp_banks = await client.sbp_banks.get_sbp_banks()
            print(f"Всего банков СБП: {len(sbp_banks.list)}")
            
            for bank in sbp_banks.list[:10]:
                print(f"{bank.name} (ID: {bank.bank_id})")

    asyncio.run(get_sbp_banks())

🔐 Персональные данные
-----------------------

Создание персональных данных для СБП
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.enum import PersonalDataType
    from aioyookassa.types.params import CreatePersonalDataParams

    async def create_personal_data():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreatePersonalDataParams(
                type=PersonalDataType.SBP_PAYOUT_RECIPIENT,
                last_name="Иванов",
                first_name="Иван",
                middle_name="Иванович"
            )
            personal_data = await client.personal_data.create_personal_data(params)
            print(f"Personal Data ID: {personal_data.id}")
            print(f"Status: {personal_data.status}")

    asyncio.run(create_personal_data())

💳 Способы оплаты
-----------------

Создание сохраненного способа оплаты
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.enum import ConfirmationType
    from aioyookassa.types.params import (
        CreatePaymentMethodParams,
        PaymentMethodCardData,
        PaymentMethodConfirmation
    )

    async def create_payment_method():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreatePaymentMethodParams(
                type="bank_card",  # Required для CreatePaymentMethodParams
                card=PaymentMethodCardData(
                    number="5555555555554477",
                    expiry_month="12",
                    expiry_year="2025",
                    csc="123"
                ),
                confirmation=PaymentMethodConfirmation(
                    type=ConfirmationType.REDIRECT,
                    return_url="https://example.com/return"
                ),
                save_payment_method=True
            )
            payment_method = await client.payment_methods.create_payment_method(params)
            print(f"Payment Method ID: {payment_method.id}")

    asyncio.run(create_payment_method())

Создание платежа с сохраненным способом оплаты
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money, Confirmation
    from aioyookassa.types.enum import Currency, ConfirmationType
    from aioyookassa.types.params import CreatePaymentParams

    async def create_payment_with_saved_method():
        async with YooKassa('your_api_key', 12345) as client:
            params = CreatePaymentParams(
                amount=Money(value=1500.00, currency=Currency.RUB),
                payment_method_id="saved_payment_method_id",
                description="Платеж с сохраненной картой",
                confirmation=Confirmation(
                    type=ConfirmationType.REDIRECT,
                    return_url="https://example.com/return"
                )
            )
            payment = await client.payments.create_payment(params)
            print(f"Payment ID: {payment.id}")

    asyncio.run(create_payment_with_saved_method())

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
