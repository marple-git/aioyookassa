API модули
===========

Обзор всех доступных API модулей в aioyookassa.

Доступ к модулям
----------------

Все API модули доступны через главный клиент:

.. code-block:: python

    from aioyookassa import YooKassa

    client = YooKassa(api_key="your_key", shop_id=12345)

    # Доступные модули
    payments = client.payments          # Платежи
    refunds = client.refunds            # Возвраты
    receipts = client.receipts          # Чеки
    invoices = client.invoices          # Счета
    payment_methods = client.payment_methods  # Способы оплаты

💳 Payments API
---------------

Модуль для работы с платежами.

Основные методы
~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.types.enum import ConfirmationType, Currency
    
    # Создание платежа
    payment = await client.payments.create_payment(
        amount=PaymentAmount(value=100.00, currency=Currency.RUB),
        confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com"),
        description="Тестовый платеж"
    )

    # Получение списка платежей
    payments = await client.payments.get_payments(
        created_at=datetime(2023, 1, 1),
        status=PaymentStatus.SUCCEEDED,
        limit=10
    )

    # Получение конкретного платежа
    payment = await client.payments.get_payment("payment_id")

    # Подтверждение платежа
    payment = await client.payments.capture_payment("payment_id")

    # Отмена платежа
    payment = await client.payments.cancel_payment("payment_id")

Примеры использования
~~~~~~~~~~~~~~~~~~~~~

Создание платежа с полными параметрами
'''''''''''''''''''''''''''''''''''''''

.. code-block:: python

    from aioyookassa.types.payment import (
        PaymentAmount, Confirmation, PaymentMethod, CardInfo,
        Recipient, Customer, Receipt, PaymentItem
    )
    from aioyookassa.types.enum import (
        ConfirmationType, Currency, PaymentMethodType,
        PaymentSubject, PaymentMode
    )

    async def create_full_payment():
        # Настройка способа оплаты
        card_info = CardInfo(
            first_six="123456",
            last_four="7890",
            expiry_month="12",
            expiry_year="2025",
            card_type="Visa"
        )
        
        payment_method = PaymentMethod(
            type=PaymentMethodType.CARD,
            id="pm_123456",
            saved=False,
            card=card_info
        )
        
        # Настройка подтверждения
        confirmation = Confirmation(
            type=ConfirmationType.REDIRECT,
            return_url="https://example.com/success"
        )
        
        # Настройка получателя
        recipient = Recipient(
            account_id="123456789",
            gateway_id="123456"
        )
        
        # Настройка клиента
        customer = Customer(
            full_name="Иван Иванов",
            email="ivan@example.com",
            phone="+79001234567"
        )
        
        # Настройка чека
        receipt = Receipt(
            customer=customer,
            items=[
                PaymentItem(
                    description="Товар",
                    quantity=1,
                    amount=PaymentAmount(value=100.00, currency=Currency.RUB),
                    vat_code=1,
                    payment_subject=PaymentSubject.COMMODITY,
                    payment_mode=PaymentMode.FULL_PAYMENT
                )
            ],
            tax_system_code=1
        )
        
        # Создание платежа
        payment = await client.payments.create_payment(
            amount=PaymentAmount(value=100.00, currency=Currency.RUB),
            description="Оплата заказа #12345",
            payment_method=payment_method,
            confirmation=confirmation,
            recipient=recipient,
            receipt=receipt,
            metadata={"order_id": "12345", "user_id": "67890"}
        )
        
        return payment

💰 Refunds API
--------------

Модуль для работы с возвратами.

Основные методы
~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.types.enum import Currency
    
    # Создание возврата
    refund = await client.refunds.create_refund(
        payment_id="payment_id",
        amount=PaymentAmount(value=50.00, currency=Currency.RUB),
        description="Частичный возврат"
    )

    # Получение информации о возврате
    refund = await client.refunds.get_refund("refund_id")

    # Получение списка возвратов
    refunds = await client.refunds.get_refunds(
        payment_id="payment_id",
        limit=10
    )

Примеры использования
~~~~~~~~~~~~~~~~~~~~~

Создание возврата с деталями
'''''''''''''''''''''''''''''

.. code-block:: python

    from aioyookassa.types.refund import RefundMethod, RefundArticle
    from aioyookassa.types.enum import Currency

    async def create_detailed_refund():
        # Настройка способа возврата
        refund_method = RefundMethod(
            type="bank_card",
            account_id="123456789"
        )
        
        # Настройка статей возврата
        articles = [
            RefundArticle(
                description="Возврат товара",
                quantity=1,
                amount=PaymentAmount(value=50.00, currency=Currency.RUB),
                vat_code=1
            )
        ]
        
        # Создание возврата
        refund = await client.refunds.create_refund(
            payment_id="payment_id",
            amount=PaymentAmount(value=50.00, currency=Currency.RUB),
            description="Возврат за некачественный товар",
            refund_method=refund_method,
            articles=articles
        )
        
        return refund

🧾 Receipts API
---------------

Модуль для работы с фискальными чеками.

Основные методы
~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.types.payment import PaymentItem
    from aioyookassa.types.enum import Currency, PaymentSubject, PaymentMode
    
    # Создание чека
    receipt = await client.receipts.create_receipt(
        payment_id="payment_id",
        items=[
            PaymentItem(
                description="Товар",
                quantity=1,
                amount=PaymentAmount(value=100.00, currency=Currency.RUB),
                vat_code=1,
                payment_subject=PaymentSubject.COMMODITY,
                payment_mode=PaymentMode.FULL_PAYMENT
            )
        ],
        tax_system_code=1
    )

    # Получение информации о чеке
    receipt = await client.receipts.get_receipt("receipt_id")

    # Получение списка чеков
    receipts = await client.receipts.get_receipts(
        payment_id="payment_id",
        limit=10
    )

Примеры использования
~~~~~~~~~~~~~~~~~~~~~

Создание чека с полными данными
'''''''''''''''''''''''''''''''

.. code-block:: python

    from aioyookassa.types.payment import Settlement
    from aioyookassa.types.receipt_registration import (
        ReceiptRegistrationItem, Supplier
    )
    from aioyookassa.types.enum import Currency

    async def create_detailed_receipt():
        # Настройка поставщика
        supplier = Supplier(
            name="ООО 'Пример'",
            inn="1234567890",
            phone="+79001234567"
        )
        
        # Настройка позиций чека
        items = [
            ReceiptRegistrationItem(
                description="Товар 1",
                quantity=2,
                amount=PaymentAmount(value=100.00, currency=Currency.RUB),
                vat_code=1,
                payment_subject="commodity",
                payment_mode="full_payment",
                supplier=supplier
            ),
            ReceiptRegistrationItem(
                description="Товар 2",
                quantity=1,
                amount=PaymentAmount(value=200.00, currency=Currency.RUB),
                vat_code=1,
                payment_subject="commodity",
                payment_mode="full_payment",
                supplier=supplier
            )
        ]
        
        # Настройка расчетов
        settlements = [
            Settlement(
                type="prepayment",
                amount=PaymentAmount(value=400.00, currency=Currency.RUB)
            )
        ]
        
        # Создание чека
        receipt = await client.receipts.create_receipt(
            payment_id="payment_id",
            items=items,
            tax_system_code=1,
            settlements=settlements
        )
        
        return receipt

📄 Invoices API
---------------

Модуль для работы со счетами на оплату.

Основные методы
~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.types.enum import Currency
    
    # Создание счета
    invoice = await client.invoices.create_invoice(
        amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
        description="Счет на оплату"
    )

    # Получение информации о счете
    invoice = await client.invoices.get_invoice("invoice_id")

    # Получение списка счетов
    invoices = await client.invoices.get_invoices(limit=10)

Примеры использования
~~~~~~~~~~~~~~~~~~~~~

Создание счета с деталями
'''''''''''''''''''''''''

.. code-block:: python

    from aioyookassa.types.invoice import (
        InvoicePaymentData, InvoiceReceipt, InvoiceCartItem
    )
    from aioyookassa.types.payment import PaymentItem
    from aioyookassa.types.enum import Currency, PaymentSubject, PaymentMode

    async def create_detailed_invoice():
        # Настройка корзины
        cart_items = [
            InvoiceCartItem(
                description="Услуга 1",
                quantity=1,
                amount=PaymentAmount(value=500.00, currency=Currency.RUB),
                vat_code=1
            ),
            InvoiceCartItem(
                description="Услуга 2",
                quantity=2,
                amount=PaymentAmount(value=250.00, currency=Currency.RUB),
                vat_code=1
            )
        ]
        
        # Настройка чека
        receipt = InvoiceReceipt(
            items=[
                PaymentItem(
                    description="Услуга 1",
                    quantity=1,
                    amount=PaymentAmount(value=500.00, currency=Currency.RUB),
                    vat_code=1,
                    payment_subject=PaymentSubject.SERVICE,
                    payment_mode=PaymentMode.FULL_PAYMENT
                ),
                PaymentItem(
                    description="Услуга 2",
                    quantity=2,
                    amount=PaymentAmount(value=250.00, currency=Currency.RUB),
                    vat_code=1,
                    payment_subject=PaymentSubject.SERVICE,
                    payment_mode=PaymentMode.FULL_PAYMENT
                )
            ],
            tax_system_code=1
        )
        
        # Настройка данных платежа
        payment_data = InvoicePaymentData(
            type="bank_card",
            account_id="123456789"
        )
        
        # Создание счета
        invoice = await client.invoices.create_invoice(
            amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
            description="Счет на оплату услуг",
            cart=cart_items,
            receipt=receipt,
            payment_method=payment_data
        )
        
        return invoice

💳 Payment Methods API
---------------------

Модуль для управления способами оплаты.

Основные методы
~~~~~~~~~~~~~~~

.. code-block:: python

    # Получение списка способов оплаты
    methods = await client.payment_methods.get_payment_methods()

    # Получение конкретного способа оплаты
    method = await client.payment_methods.get_payment_method("method_id")

Примеры использования
~~~~~~~~~~~~~~~~~~~~~

Работа со способами оплаты
'''''''''''''''''''''''''''

.. code-block:: python

    async def work_with_payment_methods():
        # Получение всех доступных способов оплаты
        methods = await client.payment_methods.get_payment_methods()
        
        print("Доступные способы оплаты:")
        for method in methods.items:
            print(f"- {method.type}: {method.description}")
        
        # Получение информации о конкретном способе
        if methods.items:
            method_id = methods.items[0].id
            method = await client.payment_methods.get_payment_method(method_id)
            print(f"Детали способа оплаты: {method.type}")

Комбинированное использование
-----------------------------

Пример комплексной обработки платежа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.types.payment import PaymentItem
    from aioyookassa.types.enum import (
        ConfirmationType, Currency, PaymentSubject, PaymentMode
    )
    
    async def process_complete_payment():
        """Полный цикл обработки платежа с чеком и возвратом."""
        
        try:
            # 1. Создание платежа
            payment = await client.payments.create_payment(
                amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
                description="Комплексный платеж",
                confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com")
            )
            
            print(f"✅ Платеж создан: {payment.id}")
            
            # 2. Ожидание оплаты (в реальном приложении через webhook)
            await asyncio.sleep(2)
            
            # 3. Проверка статуса
            payment_info = await client.payments.get_payment(payment.id)
            
            if payment_info.status == PaymentStatus.SUCCEEDED:
                # 4. Создание чека
                receipt = await client.receipts.create_receipt(
                    payment_id=payment.id,
                    items=[
                        PaymentItem(
                            description="Товар",
                            quantity=1,
                            amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
                            vat_code=1,
                            payment_subject=PaymentSubject.COMMODITY,
                            payment_mode=PaymentMode.FULL_PAYMENT
                        )
                    ],
                    tax_system_code=1
                )
                
                print(f"✅ Чек создан: {receipt.id}")
                
                # 5. Создание возврата (если нужно)
                if should_refund:
                    refund = await client.refunds.create_refund(
                        payment_id=payment.id,
                        amount=PaymentAmount(value=500.00, currency=Currency.RUB),
                        description="Частичный возврат"
                    )
                    
                    print(f"✅ Возврат создан: {refund.id}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            raise

