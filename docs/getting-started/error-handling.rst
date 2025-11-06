Обработка ошибок
================

Руководство по обработке ошибок в aioyookassa.

Типы исключений
---------------

aioyookassa предоставляет иерархию исключений для различных типов ошибок:

.. code-block:: python

    from aioyookassa.exceptions import (
        APIError,                    # Базовое исключение
        InvalidRequestError,         # Неверный запрос
        InvalidCredentials,          # Неверные учетные данные
        NotFound,                    # Ресурс не найден
    )

Базовое исключение APIError
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Все исключения API наследуются от `APIError`:

.. code-block:: python

    from aioyookassa.exceptions import APIError

    try:
        payment = await client.payments.get_payment("invalid_id")
    except APIError as e:
        print(f"API Error: {e}")
        print(f"Error type: {type(e).__name__}")

Специфичные исключения
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.exceptions import NotFound, InvalidCredentials, InvalidRequestError

    try:
        payment = await client.payments.get_payment("invalid_id")
    except NotFound:
        print("Платеж не найден")
    except InvalidCredentials:
        print("Неверные учетные данные")
    except InvalidRequestError:
        print("Неверный запрос")
    except APIError as e:
        print(f"Другая ошибка API: {e}")

Практические примеры
--------------------

Обработка ошибок при создании платежа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging
    from aioyookassa.exceptions import APIError, InvalidRequestError, InvalidCredentials

    logger = logging.getLogger(__name__)

    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreatePaymentParams
    
    async def create_payment_safely(amount: float, description: str):
        """Безопасное создание платежа с обработкой ошибок."""
        
        try:
            params = CreatePaymentParams(
                amount=PaymentAmount(value=amount, currency=Currency.RUB),
                description=description
            )
            payment = await client.payments.create_payment(params)
            logger.info(f"Payment created successfully: {payment.id}")
            return payment
            
        except InvalidCredentials:
            logger.error("Invalid API credentials. Check your API key and shop ID.")
            raise ValueError("Invalid credentials")
            
        except InvalidRequestError as e:
            logger.error(f"Invalid request: {e}")
            raise ValueError(f"Invalid request: {e}")
            
        except APIError as e:
            logger.error(f"API error: {e}")
            raise RuntimeError(f"API error: {e}")
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

Обработка ошибок при получении платежа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    async def get_payment_safely(payment_id: str):
        """Безопасное получение платежа с обработкой ошибок."""
        
        try:
            payment = await client.payments.get_payment(payment_id)
            return payment
            
        except NotFound:
            logger.warning(f"Payment not found: {payment_id}")
            return None
            
        except InvalidCredentials:
            logger.error("Invalid API credentials")
            raise ValueError("Invalid credentials")
            
        except APIError as e:
            logger.error(f"API error while getting payment {payment_id}: {e}")
            raise

Обработка ошибок при работе со списками
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    async def get_payments_with_retry(max_retries: int = 3):
        """Получение списка платежей с повторными попытками."""
        from aioyookassa.types.params import GetPaymentsParams
        
        for attempt in range(max_retries):
            try:
                params = GetPaymentsParams(limit=10)
                payments = await client.payments.get_payments(params)
                return payments
                
            except APIError as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt == max_retries - 1:
                    logger.error("All attempts failed")
                    raise
                
                # Экспоненциальная задержка
                await asyncio.sleep(2 ** attempt)
                
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise

Централизованная обработка ошибок
----------------------------------

Создание декоратора для обработки ошибок
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from functools import wraps
    import logging

    logger = logging.getLogger(__name__)

    def handle_api_errors(func):
        """Декоратор для обработки ошибок API."""
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
                
            except NotFound as e:
                logger.warning(f"Resource not found in {func.__name__}: {e}")
                return None
                
            except InvalidCredentials as e:
                logger.error(f"Invalid credentials in {func.__name__}: {e}")
                raise ValueError("Invalid API credentials")
                
            except InvalidRequestError as e:
                logger.error(f"Invalid request in {func.__name__}: {e}")
                raise ValueError(f"Invalid request: {e}")
                
            except APIError as e:
                logger.error(f"API error in {func.__name__}: {e}")
                raise RuntimeError(f"API error: {e}")
                
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                raise
        
        return wrapper

    # Использование декоратора
    @handle_api_errors
    async def create_payment_decorated(amount: float, description: str):
        from aioyookassa.types.params import CreatePaymentParams
        
        params = CreatePaymentParams(
            amount=PaymentAmount(value=amount, currency=Currency.RUB),
            description=description
        )
        return await client.payments.create_payment(params)

Создание класса для обработки ошибок
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class PaymentErrorHandler:
        """Класс для централизованной обработки ошибок платежей."""
        
        def __init__(self, logger: logging.Logger):
            self.logger = logger
        
        async def create_payment(self, amount: float, description: str):
            """Создание платежа с обработкой ошибок."""
            from aioyookassa.types.params import CreatePaymentParams
            
            try:
                params = CreatePaymentParams(
                    amount=PaymentAmount(value=amount, currency=Currency.RUB),
                    description=description
                )
                return await client.payments.create_payment(params)
            except InvalidCredentials:
                self.logger.error("Invalid API credentials")
                raise ValueError("Invalid credentials")
            except InvalidRequestError as e:
                self.logger.error(f"Invalid request: {e}")
                raise ValueError(f"Invalid request: {e}")
            except APIError as e:
                self.logger.error(f"API error: {e}")
                raise RuntimeError(f"API error: {e}")
        
        async def get_payment(self, payment_id: str):
            """Получение платежа с обработкой ошибок."""
            try:
                return await client.payments.get_payment(payment_id)
            except NotFound:
                self.logger.warning(f"Payment not found: {payment_id}")
                return None
            except APIError as e:
                self.logger.error(f"API error: {e}")
                raise

    # Использование
    error_handler = PaymentErrorHandler(logger)
    payment = await error_handler.create_payment(100.0, "Test payment")

Логирование ошибок
------------------

Настройка логирования
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging
    import sys

    # Настройка логгера
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('aioyookassa.log')
        ]
    )

    logger = logging.getLogger('aioyookassa')

Структурированное логирование
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import json
    from datetime import datetime

    def log_api_error(operation: str, error: Exception, **context):
        """Структурированное логирование ошибок API."""
        
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context
        }
        
        logger.error(json.dumps(log_data, ensure_ascii=False))

    # Использование
    try:
        payment = await client.payments.create_payment(...)
    except APIError as e:
        log_api_error(
            "create_payment",
            e,
            amount=100.0,
            currency=Currency.RUB,
            user_id="12345"
        )
        raise

Мониторинг и алерты
-------------------

Отправка уведомлений об ошибках
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from typing import Optional

    class ErrorNotifier:
        """Класс для отправки уведомлений об ошибках."""
        
        def __init__(self, webhook_url: Optional[str] = None):
            self.webhook_url = webhook_url
        
        async def notify_error(self, operation: str, error: Exception, **context):
            """Отправка уведомления об ошибке."""
            
            if not self.webhook_url:
                return
            
            error_data = {
                "operation": operation,
                "error": str(error),
                "error_type": type(error).__name__,
                "context": context,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Отправка через webhook (пример)
            # await self.send_webhook(error_data)
            
            logger.error(f"Error notification sent: {error_data}")

    # Использование
    notifier = ErrorNotifier(webhook_url="https://your-webhook.com/errors")

    try:
        payment = await client.payments.create_payment(...)
    except APIError as e:
        await notifier.notify_error(
            "create_payment",
            e,
            amount=100.0,
            user_id="12345"
        )
        raise

Метрики ошибок
~~~~~~~~~~~~~~

.. code-block:: python

    from collections import defaultdict
    import time

    class ErrorMetrics:
        """Класс для сбора метрик ошибок."""
        
        def __init__(self):
            self.error_counts = defaultdict(int)
            self.error_times = []
        
        def record_error(self, error_type: str):
            """Запись ошибки в метрики."""
            self.error_counts[error_type] += 1
            self.error_times.append(time.time())
        
        def get_error_rate(self, time_window: int = 3600) -> float:
            """Получение частоты ошибок за указанный период."""
            now = time.time()
            recent_errors = [
                t for t in self.error_times 
                if now - t <= time_window
            ]
            return len(recent_errors) / (time_window / 60)  # ошибок в минуту
        
        def get_error_summary(self) -> dict:
            """Получение сводки по ошибкам."""
            return dict(self.error_counts)

    # Использование
    metrics = ErrorMetrics()

    try:
        payment = await client.payments.create_payment(...)
    except APIError as e:
        metrics.record_error(type(e).__name__)
        logger.error(f"Error recorded: {type(e).__name__}")
        raise

