"""
Пример работы с выплатами (Payouts API).

Этот пример показывает, как создавать выплаты на банковские карты,
через СБП и на кошельки ЮMoney.
"""

import asyncio
import logging

from aioyookassa import YooKassa
from aioyookassa.types.payment import Money
from aioyookassa.types.enum import Currency, PayoutStatus
from aioyookassa.types.params import (
    CreatePayoutParams,
    BankCardPayoutDestinationData,
    BankCardPayoutCardData,
    SbpPayoutDestinationData,
    YooMoneyPayoutDestinationData,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def create_bank_card_payout():
    """Создание выплаты на банковскую карту."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("💳 Создание выплаты на банковскую карту...")
        
        params = CreatePayoutParams(
            amount=Money(value=5000.00, currency=Currency.RUB),
            payout_destination_data=BankCardPayoutDestinationData(
                card=BankCardPayoutCardData(number="5555555555554477")
            ),
            description="Выплата по договору #12345",
            metadata={"contract_id": "12345", "recipient": "Иван Иванов"}
        )
        
        payout = await client.payouts.create_payout(params)
        
        logger.info(f"✅ Выплата создана: {payout.id}")
        logger.info(f"💰 Сумма: {payout.amount.value} {payout.amount.currency}")
        logger.info(f"📊 Статус: {payout.status}")
        
        return payout


async def create_sbp_payout():
    """Создание выплаты через СБП."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("🏦 Создание выплаты через СБП...")
        
        # Сначала получаем список банков СБП
        sbp_banks = await client.sbp_banks.get_sbp_banks()
        logger.info(f"📋 Найдено банков СБП: {len(sbp_banks.list)}")
        
        # Выбираем банк (например, первый из списка)
        if sbp_banks.list:
            bank_id = sbp_banks.list[0].bank_id
            logger.info(f"🏦 Используем банк: {sbp_banks.list[0].name} (ID: {bank_id})")
        
        params = CreatePayoutParams(
            amount=Money(value=3000.00, currency=Currency.RUB),
            payout_destination_data=SbpPayoutDestinationData(
                bank_id="100000000111",  # ID банка из списка СБП
                phone="79001234567"
            ),
            description="Выплата через СБП",
            metadata={"payment_type": "sbp"}
        )
        
        payout = await client.payouts.create_payout(params)
        
        logger.info(f"✅ Выплата через СБП создана: {payout.id}")
        logger.info(f"💰 Сумма: {payout.amount.value} {payout.amount.currency}")
        
        return payout


async def create_yoomoney_payout():
    """Создание выплаты на кошелек ЮMoney."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("💼 Создание выплаты на кошелек ЮMoney...")
        
        params = CreatePayoutParams(
            amount=Money(value=2000.00, currency=Currency.RUB),
            payout_destination_data=YooMoneyPayoutDestinationData(
                account_number="41001614575714"
            ),
            description="Выплата на кошелек ЮMoney",
            metadata={"wallet_type": "yoomoney"}
        )
        
        payout = await client.payouts.create_payout(params)
        
        logger.info(f"✅ Выплата на ЮMoney создана: {payout.id}")
        logger.info(f"💰 Сумма: {payout.amount.value} {payout.amount.currency}")
        
        return payout


async def get_payout_info(payout_id: str):
    """Получение информации о выплате."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"📋 Получение информации о выплате {payout_id}...")
        
        payout = await client.payouts.get_payout(payout_id)
        
        logger.info(f"💰 Сумма: {payout.amount.value} {payout.amount.currency}")
        logger.info(f"📊 Статус: {payout.status}")
        logger.info(f"📝 Описание: {payout.description}")
        
        if payout.status == PayoutStatus.SUCCEEDED:
            logger.info("✅ Выплата успешно выполнена")
        elif payout.status == PayoutStatus.CANCELED:
            logger.info("❌ Выплата отменена")
            if payout.cancellation_details:
                logger.info(f"Причина: {payout.cancellation_details.reason}")
        
        return payout


async def main():
    """Основная функция с примерами использования."""
    try:
        # Пример 1: Выплата на банковскую карту
        payout1 = await create_bank_card_payout()
        await get_payout_info(payout1.id)
        
        # Пример 2: Выплата через СБП
        # payout2 = await create_sbp_payout()
        # await get_payout_info(payout2.id)
        
        # Пример 3: Выплата на ЮMoney
        # payout3 = await create_yoomoney_payout()
        # await get_payout_info(payout3.id)
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())

