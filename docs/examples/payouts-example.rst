Пример работы с выплатами
===========================

Полный пример создания и обработки выплат через различные способы получения.

Полный код
----------

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import Money
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import (
        CreatePayoutParams,
        BankCardPayoutDestinationData,
        BankCardPayoutCardData,
        SbpPayoutDestinationData,
        YooMoneyPayoutDestinationData
    )

    async def process_payouts():
        """Обработка выплат через различные способы."""
        
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            
            # 1. Выплата на банковскую карту
            print("Создание выплаты на банковскую карту...")
            params = CreatePayoutParams(
                amount=Money(value=1000.00, currency=Currency.RUB),
                payout_destination_data=BankCardPayoutDestinationData(
                    card=BankCardPayoutCardData(number="5555555555554477")
                ),
                description="Выплата по договору #12345"
            )
            payout = await client.payouts.create_payout(params)
            print(f"✅ Выплата создана: {payout.id}")
            print(f"📊 Статус: {payout.status}")
            
            # 2. Выплата через СБП
            print("\nСоздание выплаты через СБП...")
            # Сначала получаем список банков СБП
            banks = await client.sbp_banks.get_sbp_banks()
            if banks.list:
                bank_id = banks.list[0].bank_id  # Используем первый банк из списка
                
                params = CreatePayoutParams(
                    amount=Money(value=2000.00, currency=Currency.RUB),
                    payout_destination_data=SbpPayoutDestinationData(
                        bank_id=bank_id,
                        phone="79000000000"
                    ),
                    description="Выплата через СБП"
                )
                payout = await client.payouts.create_payout(params)
                print(f"✅ Выплата через СБП создана: {payout.id}")
            
            # 3. Выплата на кошелек ЮMoney
            print("\nСоздание выплаты на кошелек ЮMoney...")
            params = CreatePayoutParams(
                amount=Money(value=1500.00, currency=Currency.RUB),
                payout_destination_data=YooMoneyPayoutDestinationData(
                    account_number="41001614575714"
                ),
                description="Выплата на кошелек"
            )
            payout = await client.payouts.create_payout(params)
            print(f"✅ Выплата на кошелек создана: {payout.id}")
            
            # 4. Проверка статуса выплаты
            payout_info = await client.payouts.get_payout(payout.id)
            print(f"\n📊 Информация о выплате:")
            print(f"   ID: {payout_info.id}")
            print(f"   Статус: {payout_info.status}")
            print(f"   Сумма: {payout_info.amount.value} {payout_info.amount.currency}")
            if payout_info.succeeded_at:
                print(f"   Выполнена: {payout_info.succeeded_at}")

    if __name__ == "__main__":
        asyncio.run(process_payouts())

Пошаговое объяснение
--------------------

1. **Выплата на банковскую карту**
   - Указываем номер карты получателя
   - Сумму и валюту
   - Описание выплаты

2. **Выплата через СБП**
   - Получаем список банков СБП
   - Выбираем банк получателя
   - Указываем телефон получателя

3. **Выплата на кошелек ЮMoney**
   - Указываем номер кошелька
   - Сумму и валюту

4. **Проверка статуса**
   - Получаем актуальную информацию о выплате
   - Проверяем статус выполнения

