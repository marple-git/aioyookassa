Базовый пример платежа
======================

Простой пример создания и обработки платежа.

Полный код
----------

.. code-block:: python

    import asyncio
    from datetime import datetime
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount, Confirmation
    from aioyookassa.types.enum import PaymentStatus, ConfirmationType, Currency
    from aioyookassa.types.params import CreatePaymentParams, GetPaymentsParams
    from aioyookassa.exceptions import APIError, NotFound

    async def process_payment():
        """Обработка платежа с полным циклом."""
        
        # Инициализация клиента
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            
            try:
                # 1. Создание платежа
                print("Создание платежа...")
                params = CreatePaymentParams(
                    amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
                    confirmation=Confirmation(
                        type=ConfirmationType.REDIRECT, 
                        return_url="https://example.com/success"
                    ),
                    description="Оплата заказа #12345",
                    metadata={"order_id": "12345", "user_id": "67890"}
                )
                payment = await client.payments.create_payment(params)
                
                print(f"✅ Платеж создан: {payment.id}")
                print(f"🔗 URL для оплаты: {payment.confirmation.url}")
                
                # 2. Ожидание оплаты (в реальном приложении это делается через webhook)
                print("Ожидание оплаты...")
                await asyncio.sleep(2)  # Имитация ожидания
                
                # 3. Проверка статуса платежа
                payment_info = await client.payments.get_payment(payment.id)
                print(f"📊 Статус платежа: {payment_info.status}")
                
                # 4. Подтверждение платежа (если нужно)
                if payment_info.status == PaymentStatus.WAITING_FOR_CAPTURE:
                    print("Подтверждение платежа...")
                    captured_payment = await client.payments.capture_payment(payment.id)
                    print(f"✅ Платеж подтвержден: {captured_payment.status}")
                
                # 5. Получение списка платежей за сегодня
                today = datetime.now()
                params = GetPaymentsParams(
                    created_at=today,
                    status=PaymentStatus.SUCCEEDED,
                    limit=5
                )
                recent_payments = await client.payments.get_payments(params)
                
                print(f"📈 Успешных платежей сегодня: {len(recent_payments.list)}")
                
            except NotFound:
                print("❌ Платеж не найден")
            except APIError as e:
                print(f"❌ Ошибка API: {e}")
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")

    # Запуск
    if __name__ == "__main__":
        asyncio.run(process_payment())

Пошаговое объяснение
--------------------

1. **Инициализация клиента**
   - Создаем клиент с API ключом и ID магазина
   - Используем контекстный менеджер для автоматического закрытия

2. **Создание платежа**
   - Указываем сумму и валюту
   - Настраиваем подтверждение (redirect на страницу оплаты)
   - Добавляем описание и метаданные

3. **Обработка результата**
   - Получаем ID платежа и URL для оплаты
   - В реальном приложении пользователь переходит по URL для оплаты

4. **Проверка статуса**
   - Получаем актуальную информацию о платеже
   - Проверяем статус (ожидание, успех, ошибка)

5. **Подтверждение платежа**
   - Если платеж требует подтверждения, вызываем capture_payment
   - Это списывает деньги с карты пользователя

6. **Дополнительная аналитика**
   - Получаем список успешных платежей за день
   - Можно использовать для отчетности

Обработка ошибок
----------------

В примере показана базовая обработка ошибок:

- **NotFound** — платеж не найден
- **APIError** — общие ошибки API
- **Exception** — неожиданные ошибки

В продакшене рекомендуется более детальная обработка ошибок с логированием.
