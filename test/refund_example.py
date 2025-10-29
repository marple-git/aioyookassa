"""
Пример использования API для работы с возвратами (refunds)
"""
import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

from aioyookassa import YooKassa
from aioyookassa.types import Refund, RefundSource
from aioyookassa.types.payment import (Customer, PaymentAmount, PaymentItem,
                                       Receipt)


async def main():
    # Инициализация клиента
    load_dotenv()
    api_key = os.getenv("YOOKASSA_KEY")
    shop_id = os.getenv("YOOKASSA_SHOP_ID")
    client = YooKassa(api_key=api_key, shop_id=shop_id)

    # ID платежа, для которого создаем возврат
    # В реальном приложении этот ID нужно получить из вашей БД
    payment_id = "2d0f8b27-0003-5000-8000-0e2e56c06d4e"

    # Пример 1: Простой возврат
    print("=== Создание простого возврата ===")
    refund = await client.refunds.create_refund(
        payment_id=payment_id,
        amount=PaymentAmount(value=100.00, currency="RUB"),
        description="Возврат по заявлению покупателя"
    )
    
    print(f"Возврат создан: {refund.id}")
    print(f"Статус: {refund.status}")
    print(f"Сумма: {refund.amount.value} {refund.amount.currency}")
    print(f"Создан: {refund.created_at}")

    # Пример 2: Возврат с чеком
    print("\n=== Создание возврата с чеком ===")
    
    receipt_items = [
        PaymentItem(
            description="Товар 1",
            amount=PaymentAmount(value=50.00, currency="RUB"),
            vat_code=2,
            quantity="1.000",
            measure="piece",
            payment_subject="commodity",
            payment_mode="full_payment",
        ),
    ]

    receipt = Receipt(
        customer=Customer(
            email="customer@example.com",
            phone="79000000000",
        ),
        items=receipt_items,
        internet=True,
    )

    refund_with_receipt = await client.refunds.create_refund(
        payment_id=payment_id,
        amount=PaymentAmount(value=50.00, currency="RUB"),
        description="Возврат с чеком",
        receipt=receipt
    )
    
    print(f"Возврат с чеком создан: {refund_with_receipt.id}")
    print(f"Статус регистрации чека: {refund_with_receipt.receipt_registration}")

    # Пример 3: Возврат для сплитованного платежа
    print("\n=== Создание возврата для сплитованного платежа ===")
    
    sources = [
        RefundSource(
            account_id="123456",
            amount=PaymentAmount(value=75.00, currency="RUB"),
            platform_fee_amount=PaymentAmount(value=5.00, currency="RUB")
        )
    ]

    refund_split = await client.refunds.create_refund(
        payment_id=payment_id,
        amount=PaymentAmount(value=75.00, currency="RUB"),
        description="Возврат сплитованного платежа",
        sources=sources
    )
    
    print(f"Возврат для сплитования создан: {refund_split.id}")

    # Получение информации о возврате
    print("\n=== Получение информации о возврате ===")
    refund_info = await client.refunds.get_refund(refund.id)
    print(f"Возврат {refund_info.id}")
    print(f"Платеж: {refund_info.payment_id}")
    print(f"Статус: {refund_info.status}")
    print(f"Сумма: {refund_info.amount.value} {refund_info.amount.currency}")
    
    if refund_info.cancellation_details:
        print(f"Отменен: {refund_info.cancellation_details.party} - "
              f"{refund_info.cancellation_details.reason}")

    # Получение списка возвратов
    print("\n=== Получение списка возвратов ===")
    
    # Все возвраты с фильтрацией
    refunds_list = await client.refunds.get_refunds(
        limit=10,
        status="succeeded"
    )
    
    print(f"Найдено возвратов: {len(refunds_list.list)}")
    for r in refunds_list.list:
        print(f"  - {r.id}: {r.status}, {r.amount.value} {r.amount.currency}")

    # Возвраты для конкретного платежа
    print("\n=== Возвраты для конкретного платежа ===")
    payment_refunds = await client.refunds.get_refunds(
        payment_id=payment_id,
        limit=10
    )
    
    print(f"Возвратов для платежа {payment_id}: {len(payment_refunds.list)}")
    for r in payment_refunds.list:
        print(f"  - {r.id}: {r.status}, {r.amount.value} {r.amount.currency}")

    # Возвраты за период
    print("\n=== Возвраты за период ===")
    from datetime import timedelta
    
    date_from = datetime.now(timezone.utc) - timedelta(days=7)
    date_to = datetime.now(timezone.utc)
    
    period_refunds = await client.refunds.get_refunds(
        created_at_gte=date_from,
        created_at_lte=date_to,
        limit=10
    )
    
    print(f"Возвратов за последние 7 дней: {len(period_refunds.list)}")
    
    # Пагинация
    if period_refunds.next_cursor:
        print("\n=== Пагинация ===")
        next_page = await client.refunds.get_refunds(
            cursor=period_refunds.next_cursor,
            limit=10
        )
        print(f"Следующая страница: {len(next_page.list)} возвратов")


if __name__ == "__main__":
    asyncio.run(main())

