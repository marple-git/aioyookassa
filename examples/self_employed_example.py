"""
Пример работы с самозанятыми (Self-Employed API).

Этот пример показывает, как создавать объекты самозанятых
и работать с ними для выплат с чеками.
"""

import asyncio
import logging

from aioyookassa import YooKassa
from aioyookassa.types.enum import SelfEmployedStatus
from aioyookassa.types.params import (
    CreateSelfEmployedParams,
    SelfEmployedConfirmationData,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def create_self_employed():
    """Создание объекта самозанятого."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("👤 Создание объекта самозанятого...")
        
        params = CreateSelfEmployedParams(
            itn="123456789012",  # ИНН самозанятого
            confirmation=SelfEmployedConfirmationData(
                type="redirect",
                confirmation_url="https://example.com/confirm"
            ),
            metadata={"user_id": "12345", "name": "Иван Иванов"}
        )
        
        self_employed = await client.self_employed.create_self_employed(params)
        
        logger.info(f"✅ Самозанятый создан: {self_employed.id}")
        logger.info(f"📊 Статус: {self_employed.status}")
        logger.info(f"📝 ИНН: {self_employed.itn}")
        
        if self_employed.status == SelfEmployedStatus.REQUIRES_ACTION:
            logger.info("⚠️ Требуется подтверждение")
            if self_employed.confirmation:
                logger.info(f"🔗 URL подтверждения: {self_employed.confirmation.confirmation_url}")
        elif self_employed.status == SelfEmployedStatus.ACTIVE:
            logger.info("✅ Самозанятый активен")
        
        return self_employed


async def get_self_employed_info(self_employed_id: str):
    """Получение информации о самозанятом."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"📋 Получение информации о самозанятом {self_employed_id}...")
        
        self_employed = await client.self_employed.get_self_employed(self_employed_id)
        
        logger.info(f"📊 Статус: {self_employed.status}")
        logger.info(f"📝 ИНН: {self_employed.itn}")
        
        if self_employed.status == SelfEmployedStatus.ACTIVE:
            logger.info("✅ Самозанятый активен и готов к выплатам")
        elif self_employed.status == SelfEmployedStatus.REQUIRES_ACTION:
            logger.info("⚠️ Требуется подтверждение")
        elif self_employed.status == SelfEmployedStatus.CANCELED:
            logger.info("❌ Самозанятый отменен")
            if self_employed.cancellation_details:
                logger.info(f"Причина: {self_employed.cancellation_details.reason}")
        
        return self_employed


async def main():
    """Основная функция с примерами использования."""
    try:
        # Пример 1: Создание самозанятого
        self_employed = await create_self_employed()
        
        # Пример 2: Получение информации о самозанятом
        await get_self_employed_info(self_employed.id)
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())

