"""
Пример работы с участниками СБП (SBP Banks API).

Этот пример показывает, как получить список банков
Системы быстрых платежей.
"""

import asyncio
import logging

from aioyookassa import YooKassa

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def get_sbp_banks():
    """Получение списка участников СБП."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("🏦 Получение списка участников СБП...")
        
        sbp_banks = await client.sbp_banks.get_sbp_banks()
        
        logger.info(f"📊 Всего участников СБП: {len(sbp_banks.list)}")
        logger.info("")
        
        # Выводим информацию о первых 10 банках
        for i, bank in enumerate(sbp_banks.list[:10], 1):
            logger.info(f"{i}. {bank.name}")
            logger.info(f"   ID: {bank.bank_id}")
            logger.info(f"   Логотип: {bank.logo_url if bank.logo_url else 'Нет'}")
            logger.info("")
        
        return sbp_banks


async def find_bank_by_name(bank_name: str):
    """Поиск банка по названию."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"🔍 Поиск банка '{bank_name}'...")
        
        sbp_banks = await client.sbp_banks.get_sbp_banks()
        
        # Ищем банк по названию (регистронезависимый поиск)
        found_banks = [
            bank for bank in sbp_banks.list
            if bank_name.lower() in bank.name.lower()
        ]
        
        if found_banks:
            logger.info(f"✅ Найдено банков: {len(found_banks)}")
            for bank in found_banks:
                logger.info(f"  - {bank.name} (ID: {bank.bank_id})")
        else:
            logger.info(f"❌ Банк '{bank_name}' не найден")
        
        return found_banks


async def get_bank_info_for_payout():
    """Получение информации о банке для выплаты через СБП."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("💸 Получение списка банков для выплаты через СБП...")
        
        sbp_banks = await client.sbp_banks.get_sbp_banks()
        
        # Выбираем популярные банки
        popular_banks = [
            "Сбербанк", "ВТБ", "Альфа-Банк", "Тинькофф",
            "Райффайзенбанк", "Газпромбанк"
        ]
        
        logger.info("🏦 Популярные банки для выплат:")
        for bank_name in popular_banks:
            # Ищем банк по названию (регистронезависимый поиск)
            found_banks = [
                bank for bank in sbp_banks.list
                if bank_name.lower() in bank.name.lower()
            ]
            if found_banks:
                logger.info(f"  ✅ {bank_name} найден (ID: {found_banks[0].bank_id})")
            else:
                logger.info(f"  ❌ {bank_name} не найден")
        
        return sbp_banks


async def main():
    """Основная функция с примерами использования."""
    try:
        # Пример 1: Получение списка всех банков СБП
        banks = await get_sbp_banks()
        
        # Пример 2: Поиск конкретного банка
        # await find_bank_by_name("Сбербанк")
        
        # Пример 3: Получение информации для выплат
        # await get_bank_info_for_payout()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())

