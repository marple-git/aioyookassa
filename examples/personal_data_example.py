"""
Пример работы с персональными данными (Personal Data API).

Этот пример показывает, как создавать персональные данные
для выплат с проверкой получателя (СБП) и для выписок из реестра.
"""

import asyncio
import logging

from aioyookassa import YooKassa
from aioyookassa.types.enum import PersonalDataType, PersonalDataStatus
from aioyookassa.types.params import CreatePersonalDataParams

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def create_personal_data_for_sbp():
    """Создание персональных данных для выплаты через СБП с проверкой получателя."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("🔐 Создание персональных данных для СБП...")
        
        params = CreatePersonalDataParams(
            type=PersonalDataType.SBP_PAYOUT_RECIPIENT,
            last_name="Иванов",
            first_name="Иван",
            middle_name="Иванович",
            metadata={"payout_id": "12345"}
        )
        
        personal_data = await client.personal_data.create_personal_data(params)
        
        logger.info(f"✅ Персональные данные созданы: {personal_data.id}")
        logger.info(f"📊 Статус: {personal_data.status}")
        logger.info(f"👤 ФИО: {personal_data.last_name} {personal_data.first_name} {personal_data.middle_name}")
        
        return personal_data


async def create_personal_data_for_statement():
    """Создание персональных данных для выписки из реестра."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info("📄 Создание персональных данных для выписки...")
        
        params = CreatePersonalDataParams(
            type=PersonalDataType.SBP_PAYOUT_STATEMENT_RECIPIENT,
            last_name="Петров",
            first_name="Петр",
            middle_name="Петрович",
            metadata={"statement_id": "67890"}
        )
        
        personal_data = await client.personal_data.create_personal_data(params)
        
        logger.info(f"✅ Персональные данные созданы: {personal_data.id}")
        logger.info(f"📊 Статус: {personal_data.status}")
        
        return personal_data


async def get_personal_data_info(personal_data_id: str):
    """Получение информации о персональных данных."""
    async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
        logger.info(f"📋 Получение информации о персональных данных {personal_data_id}...")
        
        personal_data = await client.personal_data.get_personal_data(personal_data_id)
        
        logger.info(f"📊 Статус: {personal_data.status}")
        logger.info(f"📝 Тип: {personal_data.type}")
        
        if personal_data.status == PersonalDataStatus.REQUIRES_ACTION:
            logger.info("⚠️ Требуется действие от пользователя")
            if personal_data.confirmation:
                logger.info(f"🔗 URL подтверждения: {personal_data.confirmation.confirmation_url}")
        elif personal_data.status == PersonalDataStatus.SUCCEEDED:
            logger.info("✅ Персональные данные успешно подтверждены")
        elif personal_data.status == PersonalDataStatus.CANCELED:
            logger.info("❌ Персональные данные отменены")
            if personal_data.cancellation_details:
                logger.info(f"Причина: {personal_data.cancellation_details.reason}")
        
        return personal_data


async def main():
    """Основная функция с примерами использования."""
    try:
        # Пример 1: Создание персональных данных для СБП
        personal_data1 = await create_personal_data_for_sbp()
        await get_personal_data_info(personal_data1.id)
        
        # Пример 2: Создание персональных данных для выписки
        # personal_data2 = await create_personal_data_for_statement()
        # await get_personal_data_info(personal_data2.id)
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())

