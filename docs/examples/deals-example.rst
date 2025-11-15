Пример работы с безопасными сделками
=====================================

Полный пример создания и управления безопасными сделками.

Полный код
----------

.. code-block:: python

    import asyncio
    from datetime import datetime, timedelta
    from aioyookassa import YooKassa
    from aioyookassa.types.params import CreateDealParams, GetDealsParams
    from aioyookassa.types.enum import FeeMoment, DealStatus

    async def process_deals():
        """Обработка безопасных сделок."""
        
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            
            # 1. Создание безопасной сделки
            print("Создание безопасной сделки...")
            params = CreateDealParams(
                fee_moment=FeeMoment.PAYMENT_SUCCEEDED,  # Комиссия после успешной оплаты
                description="Безопасная сделка для продажи товара",
                metadata={"order_id": "12345", "product_id": "67890"}
            )
            deal = await client.deals.create_deal(params)
            print(f"✅ Сделка создана: {deal.id}")
            print(f"📊 Статус: {deal.status}")
            print(f"💰 Баланс: {deal.balance.value} {deal.balance.currency}")
            print(f"💵 Баланс выплаты: {deal.payout_balance.value} {deal.payout_balance.currency}")
            
            # 2. Получение информации о сделке
            deal_info = await client.deals.get_deal(deal.id)
            print(f"\n📋 Информация о сделке:")
            print(f"   ID: {deal_info.id}")
            print(f"   Статус: {deal_info.status}")
            print(f"   Момент комиссии: {deal_info.fee_moment}")
            print(f"   Создана: {deal_info.created_at}")
            print(f"   Истекает: {deal_info.expires_at}")
            
            # 3. Получение списка сделок с фильтрацией
            print("\nПолучение списка открытых сделок...")
            params = GetDealsParams(
                status=DealStatus.OPENED,
                limit=10
            )
            deals = await client.deals.get_deals(params)
            
            if deals.list:
                print(f"📊 Найдено сделок: {len(deals.list)}")
                for deal in deals.list:
                    print(f"   - {deal.id}: {deal.status}, баланс {deal.balance.value} {deal.balance.currency}")
            else:
                print("   Сделки не найдены")
            
            # 4. Получение сделок за последний месяц
            print("\nПолучение сделок за последний месяц...")
            month_ago = datetime.now() - timedelta(days=30)
            params = GetDealsParams(
                created_at_gte=month_ago,
                limit=20
            )
            recent_deals = await client.deals.get_deals(params)
            print(f"📊 Сделок за месяц: {len(recent_deals.list) if recent_deals.list else 0}")

    if __name__ == "__main__":
        asyncio.run(process_deals())

Пошаговое объяснение
--------------------

1. **Создание сделки**
   - Указываем момент перечисления комиссии (после оплаты или при закрытии)
   - Добавляем описание и метаданные
   - Получаем ID сделки для дальнейшей работы

2. **Получение информации**
   - Проверяем статус сделки
   - Смотрим балансы (общий и для выплаты)
   - Проверяем срок действия сделки

3. **Фильтрация сделок**
   - Получаем только открытые сделки
   - Используем лимит для пагинации

4. **Аналитика**
   - Получаем сделки за определенный период
   - Используем для отчетности

