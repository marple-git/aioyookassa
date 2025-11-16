Пример работы с возвратами
===========================

Полный пример создания и обработки возвратов, включая полные и частичные возвраты.

Полный возврат
--------------

Возврат всей суммы платежа.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreateRefundParams

    async def create_full_refund():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            # Получаем информацию о платеже
            payment = await client.payments.get_payment("payment_id")
            
            # Создаем полный возврат
            params = CreateRefundParams(
                payment_id=payment.id,
                amount=Money(
                    value=payment.amount.value,
                    currency=payment.amount.currency
                ),
                description="Полный возврат по заказу #12345",
                metadata={"order_id": "12345", "reason": "customer_request"}
            )
            
            refund = await client.refunds.create_refund(params)
            
            print(f"✅ Возврат создан: {refund.id}")
            print(f"💰 Сумма возврата: {refund.amount.value} {refund.amount.currency}")
            print(f"📊 Статус: {refund.status}")

    asyncio.run(create_full_refund())

Частичный возврат
-----------------

Возврат части суммы платежа.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreateRefundParams

    async def create_partial_refund():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            payment = await client.payments.get_payment("payment_id")
            
            # Создаем частичный возврат (50% от суммы)
            refund_amount = payment.amount.value * 0.5
            
            params = CreateRefundParams(
                payment_id=payment.id,
                amount=Money(value=refund_amount, currency=payment.amount.currency),
                description="Частичный возврат - возврат одного товара",
                metadata={
                    "order_id": "12345",
                    "item_id": "ITEM-001",
                    "reason": "defective_product"
                }
            )
            
            refund = await client.refunds.create_refund(params)
            
            print(f"✅ Частичный возврат создан: {refund.id}")
            print(f"💰 Сумма возврата: {refund.amount.value} {refund.amount.currency}")
            print(f"📊 Оригинальная сумма платежа: {payment.amount.value} {payment.amount.currency}")

    asyncio.run(create_partial_refund())

Множественные возвраты
----------------------

Пример создания нескольких возвратов для одного платежа.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreateRefundParams

    async def create_multiple_refunds():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            payment = await client.payments.get_payment("payment_id")
            
            # Список товаров для возврата
            items_to_refund = [
                {"id": "ITEM-001", "amount": 1000.00, "reason": "defective"},
                {"id": "ITEM-002", "amount": 500.00, "reason": "wrong_size"},
            ]
            
            refunds = []
            for item in items_to_refund:
                params = CreateRefundParams(
                    payment_id=payment.id,
                    amount=Money(value=item["amount"], currency=payment.amount.currency),
                    description=f"Возврат товара {item['id']}",
                    metadata={
                        "order_id": "12345",
                        "item_id": item["id"],
                        "reason": item["reason"]
                    }
                )
                refund = await client.refunds.create_refund(params)
                refunds.append(refund)
                print(f"✅ Возврат {refund.id} создан для товара {item['id']}")
            
            return refunds

    asyncio.run(create_multiple_refunds())

Получение информации о возврате
--------------------------------

Пример получения детальной информации о возврате.

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.enum import RefundStatus

    async def get_refund_info(refund_id: str):
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            refund = await client.refunds.get_refund(refund_id)
            
            print(f"📋 Информация о возврате:")
            print(f"   ID: {refund.id}")
            print(f"   Платеж: {refund.payment_id}")
            print(f"   Сумма: {refund.amount.value} {refund.amount.currency}")
            print(f"   Статус: {refund.status}")
            print(f"   Описание: {refund.description}")
            
            if refund.status == RefundStatus.SUCCEEDED:
                print(f"   ✅ Возврат успешно выполнен")
                if refund.succeeded_at:
                    print(f"   Время выполнения: {refund.succeeded_at}")
            elif refund.status == RefundStatus.CANCELED:
                print(f"   ❌ Возврат отменен")
                if refund.cancellation_details:
                    print(f"   Причина: {refund.cancellation_details.reason}")

    asyncio.run(get_refund_info("refund_id"))

Получение списка возвратов
---------------------------

Пример получения списка возвратов с фильтрацией.

.. code-block:: python

    import asyncio
    from datetime import datetime
    from aioyookassa import YooKassa
    from aioyookassa.types.enum import RefundStatus
    from aioyookassa.types.params import GetRefundsParams

    async def get_refunds_list():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            # Получение всех возвратов
            refunds = await client.refunds.get_refunds()
            print(f"📊 Всего возвратов: {len(refunds.list)}")
            
            # Получение возвратов с фильтрами
            params = GetRefundsParams(
                payment_id="payment_id",  # Возвраты для конкретного платежа
                status=RefundStatus.SUCCEEDED,
                limit=10
            )
            filtered_refunds = await client.refunds.get_refunds(params)
            
            print(f"📊 Успешных возвратов: {len(filtered_refunds.list)}")
            for refund in filtered_refunds.list:
                print(f"  - {refund.id}: {refund.amount.value} {refund.amount.currency}")

    asyncio.run(get_refunds_list())

