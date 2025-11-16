"""
Пример работы с сохраненными способами оплаты (Payment Methods API).

Этот пример показывает, как создавать и использовать
сохраненные способы оплаты для повторных платежей.
"""

import asyncio
import logging

from aioyookassa import YooKassa
from aioyookassa.types.payment import Money, Confirmation
from aioyookassa.types.enum import Currency, ConfirmationType
from aioyookassa.types.params import (
    CreatePaymentMethodParams,
    PaymentMethodCardData,
    PaymentMethodConfirmation,
    CreatePaymentParams,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def create_payment_method():
    """Создание сохраненного способа оплаты."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("💳 Создание сохраненного способа оплаты...")
        
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
            save_payment_method=True,
            metadata={"user_id": "12345", "card_name": "Основная карта"}
        )
        
        payment_method = await client.payment_methods.create_payment_method(params)
        
        logger.info(f"✅ Способ оплаты создан: {payment_method.id}")
        logger.info(f"📊 Тип: {payment_method.type}")
        
        if payment_method.confirmation:
            logger.info(f"🔗 URL подтверждения: {payment_method.confirmation.confirmation_url}")
        
        return payment_method


async def get_payment_method(payment_method_id: str):
    """Получение информации о сохраненном способе оплаты."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"📋 Получение информации о способе оплаты {payment_method_id}...")
        
        payment_method = await client.payment_methods.get_payment_method(payment_method_id)
        
        logger.info(f"📊 Тип: {payment_method.type}")
        logger.info(f"💳 Сохранен: {payment_method.saved}")
        
        if payment_method.card:
            logger.info(f"💳 Карта: ****{payment_method.card.last4}")
            logger.info(f"📅 Срок действия: {payment_method.card.expiry_month}/{payment_method.card.expiry_year}")
        
        return payment_method


async def create_payment_with_saved_method(payment_method_id: str):
    """Создание платежа с использованием сохраненного способа оплаты."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"💳 Создание платежа с сохраненным способом оплаты {payment_method_id}...")
        
        params = CreatePaymentParams(
            amount=Money(value=1500.00, currency=Currency.RUB),
            payment_method_id=payment_method_id,  # Используем сохраненный способ оплаты
            description="Платеж с сохраненной картой",
            confirmation=Confirmation(
                type=ConfirmationType.REDIRECT,
                return_url="https://example.com/return"
            ),
            metadata={"order_id": "67890", "payment_method": "saved"}
        )
        
        payment = await client.payments.create_payment(params)
        
        logger.info(f"✅ Платеж создан: {payment.id}")
        logger.info(f"💰 Сумма: {payment.amount.value} {payment.amount.currency}")
        
        if payment.confirmation:
            logger.info(f"🔗 URL для оплаты: {payment.confirmation.url}")
        
        return payment


async def main():
    """Основная функция с примерами использования."""
    try:
        # Пример 1: Создание сохраненного способа оплаты
        payment_method = await create_payment_method()
        
        # Пример 2: Получение информации о способе оплаты
        # await get_payment_method(payment_method.id)
        
        # Пример 3: Создание платежа с сохраненным способом оплаты
        # payment = await create_payment_with_saved_method(payment_method.id)
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())

