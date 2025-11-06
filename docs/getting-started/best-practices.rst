Лучшие практики
===============

Рекомендации по эффективному использованию aioyookassa.

Управление соединениями
-----------------------

Используйте контекстный менеджер
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # ✅ Хорошо
    async with YooKassa(api_key="key", shop_id=12345) as client:
        payment = await client.payments.create_payment(...)
        # Клиент автоматически закроется

    # ❌ Плохо
    client = YooKassa(api_key="key", shop_id=12345)
    payment = await client.payments.create_payment(...)
    # Забыли закрыть клиент!

Переиспользование клиента
~~~~~~~~~~~~~~~~~~~~~~~~~

Для высоконагруженных приложений создавайте один клиент и переиспользуйте его:

.. code-block:: python

    class PaymentService:
        def __init__(self, api_key: str, shop_id: int):
            self.client = YooKassa(api_key=api_key, shop_id=shop_id)
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            await self.client.close()
        
        async def process_payment(self, amount: float, currency: str):
            from aioyookassa.types.enum import ConfirmationType
            from aioyookassa.types.params import CreatePaymentParams
            
            params = CreatePaymentParams(
                amount=PaymentAmount(value=amount, currency=currency),
                confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com")
            )
            return await self.client.payments.create_payment(params)

Обработка ошибок
----------------

Используйте специфичные исключения
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.exceptions import APIError, NotFound, InvalidCredentials

    try:
        payment = await client.payments.get_payment("invalid_id")
    except NotFound:
        # Обработка случая, когда платеж не найден
        logger.warning("Payment not found")
    except InvalidCredentials:
        # Обработка ошибки авторизации
        logger.error("Invalid API credentials")
    except APIError as e:
        # Общая обработка ошибок API
        logger.error(f"API error: {e}")
    except Exception as e:
        # Обработка неожиданных ошибок
        logger.error(f"Unexpected error: {e}")

Логирование
~~~~~~~~~~~

Добавьте подробное логирование для отладки:

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreatePaymentParams
    
    async def create_payment_with_logging(amount: float, description: str):
        logger.info(f"Creating payment: amount={amount}, description={description}")
        
        try:
            params = CreatePaymentParams(
                amount=PaymentAmount(value=amount, currency=Currency.RUB),
                description=description
            )
            payment = await client.payments.create_payment(params)
            logger.info(f"Payment created successfully: {payment.id}")
            return payment
        except APIError as e:
            logger.error(f"Failed to create payment: {e}")
            raise

Валидация данных
----------------

Используйте Pydantic модели для валидации
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.types.payment import PaymentAmount, Confirmation
    from aioyookassa.types.enum import PaymentStatus

    def validate_payment_data(amount: float, currency: str) -> PaymentAmount:
        """Валидация данных платежа."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if currency not in ["RUB", "USD", "EUR"]:
            raise ValueError("Unsupported currency")
        
        return PaymentAmount(value=amount, currency=currency)

    # Использование
    try:
        from aioyookassa.types.params import CreatePaymentParams
        
        amount = validate_payment_data(100.0, "RUB")
        params = CreatePaymentParams(amount=amount, ...)
        payment = await client.payments.create_payment(params)
    except ValueError as e:
        logger.error(f"Validation error: {e}")

Асинхронное программирование
----------------------------

Используйте asyncio.gather для параллельных операций
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio

    async def get_multiple_payments(payment_ids: list):
        """Получение нескольких платежей параллельно."""
        tasks = [
            client.payments.get_payment(payment_id) 
            for payment_id in payment_ids
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)

    # Использование
    payment_ids = ["id1", "id2", "id3"]
    results = await get_multiple_payments(payment_ids)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Failed to get payment {payment_ids[i]}: {result}")
        else:
            logger.info(f"Payment {payment_ids[i]}: {result.status}")

Обработка таймаутов
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio

    async def create_payment_with_timeout(amount: float, timeout: int = 30):
        """Создание платежа с таймаутом."""
        from aioyookassa.types.params import CreatePaymentParams
        
        try:
            params = CreatePaymentParams(amount=amount, ...)
            return await asyncio.wait_for(
                client.payments.create_payment(params),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.error("Payment creation timed out")
            raise

Безопасность
------------

Храните секреты в переменных окружения
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from aioyookassa import YooKassa

    # ✅ Хорошо
    api_key = os.getenv("YOOKASSA_API_KEY")
    shop_id = int(os.getenv("YOOKASSA_SHOP_ID"))
    
    client = YooKassa(api_key=api_key, shop_id=shop_id)

    # ❌ Плохо
    client = YooKassa(api_key="live_1234567890", shop_id=12345)

Используйте разные ключи для тестов и продакшена
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os

    def get_client():
        """Получение клиента в зависимости от окружения."""
        if os.getenv("ENVIRONMENT") == "production":
            api_key = os.getenv("YOOKASSA_LIVE_API_KEY")
            shop_id = int(os.getenv("YOOKASSA_LIVE_SHOP_ID"))
        else:
            api_key = os.getenv("YOOKASSA_TEST_API_KEY")
            shop_id = int(os.getenv("YOOKASSA_TEST_SHOP_ID"))
        
        return YooKassa(api_key=api_key, shop_id=shop_id)

Производительность
------------------

Кэширование результатов
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from functools import lru_cache
    import asyncio

    @lru_cache(maxsize=128)
    def get_cached_payment(payment_id: str):
        """Кэширование информации о платеже."""
        return asyncio.create_task(
            client.payments.get_payment(payment_id)
        )

Ограничение частоты запросов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from collections import defaultdict

    class RateLimiter:
        def __init__(self, max_requests: int, time_window: int):
            self.max_requests = max_requests
            self.time_window = time_window
            self.requests = defaultdict(list)
        
        async def acquire(self, key: str = "default"):
            now = asyncio.get_event_loop().time()
            
            # Удаляем старые запросы
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if now - req_time < self.time_window
            ]
            
            if len(self.requests[key]) >= self.max_requests:
                sleep_time = self.time_window - (now - self.requests[key][0])
                await asyncio.sleep(sleep_time)
            
            self.requests[key].append(now)

    # Использование
    rate_limiter = RateLimiter(max_requests=100, time_window=60)  # 100 запросов в минуту

    async def create_payment_with_rate_limit(amount: float):
        from aioyookassa.types.params import CreatePaymentParams
        
        await rate_limiter.acquire()
        params = CreatePaymentParams(amount=amount, ...)
        return await client.payments.create_payment(params)

Тестирование
------------

Используйте моки для тестирования
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pytest
    from unittest.mock import AsyncMock, patch
    from aioyookassa import YooKassa

    @pytest.mark.asyncio
    async def test_create_payment():
        with patch('aioyookassa.core.api.payments.PaymentsAPI.create_payment') as mock_create:
            mock_create.return_value = AsyncMock()
            mock_create.return_value.id = "test_payment_id"
            
            from aioyookassa.types.enum import Currency
            from aioyookassa.types.params import CreatePaymentParams
            
            client = YooKassa(api_key="test", shop_id=12345)
            params = CreatePaymentParams(
                amount=PaymentAmount(value=100, currency=Currency.RUB),
                description="Test"
            )
            payment = await client.payments.create_payment(params)
            
            assert payment.id == "test_payment_id"
            mock_create.assert_called_once()

Используйте тестовые данные
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @pytest.fixture
    def sample_payment_data():
        return {
            "id": "test_payment_id",
            "status": "succeeded",
            "amount": {"value": "100.00", "currency": "RUB"},
            "description": "Test payment"
        }

    @pytest.mark.asyncio
    async def test_payment_creation(sample_payment_data):
        # Тест с использованием фикстуры
        pass

