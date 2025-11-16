Продвинутый пример работы с платежами
======================================

Примеры продвинутого использования API платежей, включая работу с метаданными,
обработку различных статусов и интеграцию с бизнес-логикой.

Работа с метаданными
--------------------

Метаданные позволяют хранить дополнительную информацию о платеже,
которая будет возвращена в webhook-уведомлениях.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money, Confirmation
    from aioyookassa.types.enum import Currency, ConfirmationType
    from aioyookassa.types.params import CreatePaymentParams

    async def create_payment_with_metadata():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            params = CreatePaymentParams(
                amount=Money(value=5000.00, currency=Currency.RUB),
                confirmation=Confirmation(
                    type=ConfirmationType.REDIRECT,
                    return_url="https://example.com/return"
                ),
                description="Платеж с метаданными",
                metadata={
                    "order_id": "12345",
                    "user_id": "67890",
                    "product_id": "PROD-001",
                    "category": "electronics",
                    "promo_code": "SUMMER2024"
                }
            )
            payment = await client.payments.create_payment(params)
            
            print(f"Payment ID: {payment.id}")
            print(f"Metadata: {payment.metadata}")

    asyncio.run(create_payment_with_metadata())

Обработка различных статусов платежа
-------------------------------------

Пример обработки всех возможных статусов платежа.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.enum import PaymentStatus

    async def handle_payment_status(payment_id: str):
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            payment = await client.payments.get_payment(payment_id)
            
            if payment.status == PaymentStatus.PENDING:
                print("⏳ Платеж ожидает оплаты")
                print(f"URL для оплаты: {payment.confirmation.url}")
                
            elif payment.status == PaymentStatus.WAITING_FOR_CAPTURE:
                print("⏸️ Платеж ожидает подтверждения")
                # Подтверждаем платеж
                captured = await client.payments.capture_payment(payment_id)
                print(f"✅ Платеж подтвержден: {captured.status}")
                
            elif payment.status == PaymentStatus.SUCCEEDED:
                print("✅ Платеж успешно выполнен")
                if payment.succeeded_at:
                    print(f"Время выполнения: {payment.succeeded_at}")
                    
            elif payment.status == PaymentStatus.CANCELED:
                print("❌ Платеж отменен")
                if payment.cancellation_details:
                    print(f"Причина: {payment.cancellation_details.reason}")
                    print(f"Партия: {payment.cancellation_details.party}")

    asyncio.run(handle_payment_status("payment_id"))

Пакетная обработка платежей
----------------------------

Пример создания нескольких платежей одновременно.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money, Confirmation
    from aioyookassa.types.enum import Currency, ConfirmationType
    from aioyookassa.types.params import CreatePaymentParams

    async def create_multiple_payments():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            orders = [
                {"id": "1", "amount": 1000.00, "description": "Заказ #1"},
                {"id": "2", "amount": 2000.00, "description": "Заказ #2"},
                {"id": "3", "amount": 3000.00, "description": "Заказ #3"},
            ]
            
            payments = []
            for order in orders:
                params = CreatePaymentParams(
                    amount=Money(value=order["amount"], currency=Currency.RUB),
                    confirmation=Confirmation(
                        type=ConfirmationType.REDIRECT,
                        return_url="https://example.com/return"
                    ),
                    description=order["description"],
                    metadata={"order_id": order["id"]}
                )
                payment = await client.payments.create_payment(params)
                payments.append(payment)
                print(f"✅ Создан платеж {payment.id} для заказа {order['id']}")
            
            return payments

    asyncio.run(create_multiple_payments())

Интеграция с базой данных
-------------------------

Пример сохранения информации о платеже в базу данных.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money, Confirmation
    from aioyookassa.types.enum import Currency, ConfirmationType, PaymentStatus
    from aioyookassa.types.params import CreatePaymentParams

    # Пример с использованием SQLAlchemy (адаптируйте под вашу БД)
    async def create_payment_with_db():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            # Создаем платеж
            params = CreatePaymentParams(
                amount=Money(value=5000.00, currency=Currency.RUB),
                confirmation=Confirmation(
                    type=ConfirmationType.REDIRECT,
                    return_url="https://example.com/return"
                ),
                description="Платеж с сохранением в БД",
                metadata={"order_id": "12345"}
            )
            payment = await client.payments.create_payment(params)
            
            # Сохраняем в БД (пример с SQLAlchemy)
            # from your_app.models import Payment
            # db_payment = Payment(
            #     yookassa_id=payment.id,
            #     amount=payment.amount.value,
            #     currency=payment.amount.currency,
            #     status=payment.status,
            #     order_id=payment.metadata.get("order_id")
            # )
            # session.add(db_payment)
            # session.commit()
            
            print(f"✅ Платеж {payment.id} создан и сохранен в БД")

    asyncio.run(create_payment_with_db())

