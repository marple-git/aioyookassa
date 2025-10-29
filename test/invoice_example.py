"""
Пример использования API для работы со счетами (invoices)
"""
import asyncio
import os
from datetime import datetime, timedelta, timezone

from aioyookassa import YooKassa
from aioyookassa.types import (
    InvoiceCartItem,
    InvoiceDeliveryMethodData,
    InvoicePaymentData,
    InvoiceReceipt,
    InvoiceReceiptItem,
)
from aioyookassa.types.payment import PaymentAmount, Customer


async def main():
    # Инициализация клиента
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("YOOKASSA_KEY")
    shop_id = os.getenv("YOOKASSA_SHOP_ID")
    client = YooKassa(api_key=api_key, shop_id=shop_id)

    # Создание товаров для корзины
    cart_items = [
        InvoiceCartItem(
            description="Товар 1",
            price=PaymentAmount(value=1000.00, currency="RUB"),
            quantity=2,
        ),
        InvoiceCartItem(
            description="Товар 2",
            price=PaymentAmount(value=500.00, currency="RUB"),
            discount_price=PaymentAmount(value=450.00, currency="RUB"),
            quantity=1,
        ),
    ]

    # Создание товаров для чека
    receipt_items = [
        InvoiceReceiptItem(
            description="Товар 1",
            amount=PaymentAmount(value=1000.00, currency="RUB"),
            vat_code=2,
            quantity="2.000",
            measure="piece",
            payment_subject="commodity",
            payment_mode="full_payment",
        ),
        InvoiceReceiptItem(
            description="Товар 2",
            amount=PaymentAmount(value=450.00, currency="RUB"),
            vat_code=2,
            quantity="1.000",
            measure="piece",
            payment_subject="commodity",
            payment_mode="full_payment",
        ),
    ]

    # Данные чека
    receipt = InvoiceReceipt(
        customer=Customer(
            email="customer@example.com",
            phone="79000000000",
        ),
        items=receipt_items,
        internet=True,
    )

    # Данные платежа
    payment_data = InvoicePaymentData(
        amount=PaymentAmount(value=2450.00, currency="RUB"),
        receipt=receipt,
        capture=True,
        description="Оплата заказа №123",
        metadata={"order_id": "123"},
    )

    # Способ доставки счета
    delivery_method_data = InvoiceDeliveryMethodData(type="self")

    # Создание счета
    # expires_at можно передать как строку в ISO 8601 или как datetime объект
    expires_at = datetime.now(timezone.utc) + timedelta(days=5)
    
    invoice = await client.invoices.create_invoice(
        payment_data=payment_data,
        cart=cart_items,
        expires_at=expires_at,  # Можно передать datetime или строку "2024-12-31T23:59:59.000Z"
        delivery_method_data=delivery_method_data,
        locale="ru_RU",
        description="Счет на оплату заказа №123",
        metadata={"internal_order_id": "ORDER-123"},
    )

    print(f"Счет создан: {invoice.id}")
    print(f"Ссылка на оплату: {invoice.url}")
    print(f"Статус: {invoice.status}")
    print(f"Срок действия: {invoice.expires_at}")

    # Получение информации о счете
    invoice_info = await client.invoices.get_invoice(invoice.id)
    print(f"\nИнформация о счете {invoice_info.id}:")
    print(f"Статус: {invoice_info.status}")
    print(f"Создан: {invoice_info.created_at}")
    
    # Примечание: API ЮКассы не поддерживает получение списка всех счетов
    # Доступно только получение информации о конкретном счете по его ID


if __name__ == "__main__":
    asyncio.run(main())

