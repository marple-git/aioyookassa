"""
Пример работы с безопасными сделками (Deals API).

Этот пример показывает, как создавать безопасные сделки
и работать с ними.
"""

import asyncio
import logging

from aioyookassa import YooKassa
from aioyookassa.types.enum import FeeMoment, DealStatus, Currency
from aioyookassa.types.payment import Money, Confirmation
from aioyookassa.types.params import CreateDealParams, CreatePaymentParams, GetDealsParams

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def create_deal():
    """Создание безопасной сделки."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("🤝 Создание безопасной сделки...")
        
        params = CreateDealParams(
            fee_moment=FeeMoment.PAYMENT_SUCCEEDED,
            description="Безопасная сделка для продажи товара",
            metadata={"order_id": "12345", "product": "Товар"}
        )
        
        deal = await client.deals.create_deal(params)
        
        logger.info(f"✅ Сделка создана: {deal.id}")
        logger.info(f"📊 Статус: {deal.status}")
        logger.info(f"💰 Момент списания комиссии: {deal.fee_moment}")
        
        return deal


async def create_payment_with_deal(deal_id: str):
    """Создание платежа с привязкой к сделке."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"💳 Создание платежа для сделки {deal_id}...")
        
        params = CreatePaymentParams(
            amount=Money(value=10000.00, currency=Currency.RUB),
            confirmation=Confirmation(
                type="redirect",
                return_url="https://example.com/return"
            ),
            description="Платеж по безопасной сделке",
            deal=deal_id,  # Привязываем платеж к сделке
            metadata={"deal_id": deal_id}
        )
        
        payment = await client.payments.create_payment(params)
        
        logger.info(f"✅ Платеж создан: {payment.id}")
        logger.info(f"🔗 URL для оплаты: {payment.confirmation.url}")
        
        return payment


async def get_deal_info(deal_id: str):
    """Получение информации о сделке."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"📋 Получение информации о сделке {deal_id}...")
        
        deal = await client.deals.get_deal(deal_id)
        
        logger.info(f"📊 Статус: {deal.status}")
        logger.info(f"💰 Момент списания комиссии: {deal.fee_moment}")
        logger.info(f"📝 Описание: {deal.description}")
        
        if deal.status == DealStatus.OPENED:
            logger.info("✅ Сделка открыта")
        elif deal.status == DealStatus.CLOSED:
            logger.info("🔒 Сделка закрыта")
        
        return deal


async def get_deals_list():
    """Получение списка сделок."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("📋 Получение списка сделок...")
        
        # Получение всех сделок
        deals = await client.deals.get_deals()
        logger.info(f"📊 Всего сделок: {len(deals.list)}")
        
        # Получение сделок с фильтрами
        params = GetDealsParams(
            status=DealStatus.OPENED,
            limit=10
        )
        filtered_deals = await client.deals.get_deals(params)
        
        logger.info(f"📊 Открытых сделок: {len(filtered_deals.list)}")
        
        for deal in filtered_deals.list:
            logger.info(f"  - Сделка {deal.id}: {deal.status}")
        
        return filtered_deals


async def main():
    """Основная функция с примерами использования."""
    try:
        # Пример 1: Создание сделки
        deal = await create_deal()
        
        # Пример 2: Получение информации о сделке
        await get_deal_info(deal.id)
        
        # Пример 3: Создание платежа с привязкой к сделке
        # payment = await create_payment_with_deal(deal.id)
        
        # Пример 4: Получение списка сделок
        await get_deals_list()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())

