Changelog
=========

История изменений aioyookassa.

Версия 2.0.0 (Текущая) ⚠️ BREAKING CHANGES
-------------------------------------------

**⚠️ ВАЖНО: Эта версия содержит критические изменения, несовместимые с версией 1.x**

**Новые возможности:**
- Объединены дублирующиеся типы для улучшения консистентности API
- Улучшена архитектура с помощью BaseAPI и BaseAPIMethod классов
- Добавлена поддержка создания способов оплаты (Payment Methods API)
- Улучшена типизация и валидация параметров

**Критические изменения (Breaking Changes):**
- **Удалены дублирующиеся типы:**
  
  .. code-block:: python
  
      # Старый код (1.x)
      from aioyookassa.types import (
          RefundCancellationDetails,
          RefundSettlement,
          ReceiptSettlement
      )
      
      # Новый код (2.0+)
      from aioyookassa.types import (
          CancellationDetails,  # Используется для всех cancellation details
          Settlement            # Используется для всех settlements
      )

- **Изменения в типах:**
  - `RefundCancellationDetails` → `CancellationDetails`
  - `RefundSettlement` → `Settlement`
  - `ReceiptSettlement` → `Settlement`

- **Изменения в API клиентах - методы теперь принимают Pydantic модели:**
  
  .. code-block:: python
  
      # Старый код (1.x)
      payment = await client.payments.create_payment(
          amount=PaymentAmount(value=100.00, currency=Currency.RUB),
          description="Test payment",
          confirmation=Confirmation(...),
          capture=False,
          client_ip="192.168.1.1"
      )
      
      # Новый код (2.0+)
      from aioyookassa.types.params import CreatePaymentParams
      
      params = CreatePaymentParams(
          amount=PaymentAmount(value=100.00, currency=Currency.RUB),
          description="Test payment",
          confirmation=Confirmation(...),
          capture=False,
          client_ip="192.168.1.1"
      )
      payment = await client.payments.create_payment(params)
      
      # Также поддерживается dict для обратной совместимости
      payment = await client.payments.create_payment({
          "amount": {"value": 100.00, "currency": "RUB"},
          "description": "Test payment"
      })

**Улучшения:**
- Рефакторинг кода для уменьшения дублирования
- Улучшена архитектура с помощью базовых классов BaseAPI и BaseAPIMethod
- Добавлены helper функции для нормализации параметров
- Улучшена типизация с помощью Pydantic моделей для параметров API
- Покрытие тестами увеличено до 92%

**Исправления:**
- Исправлены проблемы с циклическими импортами
- Улучшена обработка типов в mypy
- Исправлены проблемы с валидацией параметров

**Технические детали:**
- Python 3.8.1+ поддержка
- Зависимости: aiohttp >= 3.9.0, pydantic >= 2.0.0
- Полная совместимость с YooKassa API v3

**Руководство по миграции:**
См. раздел :ref:`migration-guide-2.0` для подробных инструкций по миграции с версии 1.x на 2.0.

Версия 1.0.3
-------------

**Улучшения:**
- Улучшена обработка параметров API
- Исправлены мелкие баги

Версия 1.0.0 ⚠️ BREAKING CHANGES
-------------------------------------------

**⚠️ ВАЖНО: Эта версия содержит критические изменения, несовместимые с версиями 0.x**

**Новые возможности:**
- Полная переработка архитектуры библиотеки
- Добавлена полная поддержка всех API модулей YooKassa
- Реализованы API для работы с платежами, возвратами, чеками и счетами
- Добавлена поддержка всех типов данных YooKassa API
- Создана система исключений для обработки ошибок
- Новый модульный подход к API (payments, refunds, receipts, invoices, payment_methods)

**Критические изменения (Breaking Changes):**
- **Изменена структура доступа к API** - теперь используется модульный подход:
  
  .. code-block:: python
  
      # Старый код (0.x)
      payment = await client.create_payment(...)
      payments = await client.get_payments(...)
      
      # Новый код (1.0+)
      payment = await client.payments.create_payment(...)
      payments = await client.payments.get_payments(...)

- **Изменена структура импортов**:
  
  .. code-block:: python
  
      # Старый код (0.x)
      from aioyookassa.core.client import YooKassa
      
      # Новый код (1.0+)
      from aioyookassa import YooKassa

- **Изменена обработка дат** - теперь используются datetime объекты вместо строк:
  
  .. code-block:: python
  
      # Старый код (0.x)
      payments = await client.get_payments(created_at="2023-01-01T00:00:00.000Z")
      
      # Новый код (1.0+)
      from datetime import datetime
      payments = await client.payments.get_payments(created_at=datetime(2023, 1, 1))

- **Изменена структура ответов** - в JSON используется ключ `items`, но в Python коде доступно поле `list`:
  
  .. code-block:: python
  
      # В Python коде (1.0+)
      for payment in payments.list:
          print(payment.id)
      
      # JSON содержит ключ "items", но Pydantic автоматически маппит его в поле "list"

- **Обновлены зависимости** - требуются новые версии:
  - Pydantic >= 2.0.0 (было 1.x)
  - aiohttp >= 3.9.0 (было 3.8.0)

**Улучшения:**
- Полная типизация с использованием Pydantic v2
- Асинхронная архитектура для высокой производительности
- Подробная документация с примерами
- 90% покрытие кода тестами
- Улучшенная система обработки ошибок
- Оптимизированная работа с HTTP соединениями

**Исправления:**
- Исправлена обработка datetime объектов в API запросах
- Улучшена система обработки ошибок
- Оптимизирована работа с HTTP соединениями
- Исправлены проблемы с типизацией

**Технические детали:**
- Python 3.8.1+ поддержка
- Зависимости: aiohttp >= 3.9.0, pydantic >= 2.0.0
- Полная совместимость с YooKassa API v3

**Руководство по миграции:**
См. раздел :ref:`migration-guide` для подробных инструкций по миграции с версии 0.x на 1.0.

Версия 0.1.6
-------------

**Новые возможности:**
- Добавлена базовая поддержка API модулей
- Реализованы базовые методы для работы с платежами

**Улучшения:**
- Улучшена документация
- Добавлены примеры использования

**Технические детали:**
- Python 3.8+ поддержка
- Зависимости: aiohttp, pydantic 1.x
- Базовая совместимость с YooKassa API v3

Версия 0.1.5
-------------

**Новые возможности:**
- Добавлена базовая поддержка платежей
- Реализован основной клиент YooKassa

**Улучшения:**
- Улучшена документация
- Добавлены примеры использования

**Исправления:**
- Исправлены ошибки в базовом клиенте

Версия 0.1.4
-------------

**Новые возможности:**
- Первая публичная версия
- Базовая функциональность для работы с API

**Технические детали:**
- Начальная реализация асинхронного клиента
- Поддержка основных операций с платежами

Планы на будущее
----------------


Версия 2.1.0 (Планируется)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Новые возможности:**
- Добавление поддержки webhook'ов для обработки уведомлений
- Расширенная система логирования с возможностью кастомизации
- Метрики и мониторинг интеграции
- Кэширование ответов API для улучшения производительности

**Улучшения:**
- Оптимизация производительности
- Расширенная документация с дополнительными примерами
- Дополнительные примеры интеграции с популярными фреймворками

Версия 3.0.0 (Долгосрочные планы)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Новые возможности:**
- Полная переработка архитектуры для улучшения производительности
- Поддержка новых функций YooKassa API
- Расширенная типизация с использованием новых возможностей Python
- Async/await оптимизации

**Улучшения:**
- Улучшенная производительность
- Расширенная документация
- Дополнительные примеры использования

**Критические изменения:**
- Возможные breaking changes для улучшения API
- Обновление минимальной версии Python до 3.10+

Миграция между версиями
-----------------------

.. _migration-guide-2.0:

Миграция с версии 1.x на 2.0.0 ⚠️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**⚠️ ВАЖНО: Версия 2.0.0 содержит критические изменения, несовместимые с версией 1.x**

Пошаговое руководство по миграции
''''''''''''''''''''''''''''''''''

1. **Обновите зависимости**
   
   Убедитесь, что у вас установлена правильная версия библиотеки:
   
   .. code-block:: bash
   
       pip install aioyookassa>=2.0.0

2. **Обновите импорты типов**
   
   .. code-block:: python
   
       # Старый код (1.x)
       from aioyookassa.types import (
           RefundCancellationDetails,
           RefundSettlement,
           ReceiptSettlement
       )
       
       # Новый код (2.0+)
       from aioyookassa.types import (
           CancellationDetails,  # Используется везде
           Settlement            # Используется везде
       )

3. **Обновите использование типов в коде**
   
   .. code-block:: python
   
       # Старый код (1.x)
       from aioyookassa.types import RefundCancellationDetails, RefundSettlement
       
       cancellation_details = RefundCancellationDetails(
           party=CancellationParty.MERCHANT,
           reason=CancellationReason.CANCELED_BY_MERCHANT
       )
       
       settlement = RefundSettlement(
           type="payout",
           amount=PaymentAmount(value=100, currency="RUB")
       )
       
       # Новый код (2.0+)
       from aioyookassa.types import CancellationDetails, Settlement
       
       cancellation_details = CancellationDetails(
           party=CancellationParty.MERCHANT,
           reason=CancellationReason.CANCELED_BY_MERCHANT
       )
       
       settlement = Settlement(
           type="payout",
           amount=PaymentAmount(value=100, currency="RUB")
       )

4. **Обновите использование ReceiptSettlement**
   
   .. code-block:: python
   
       # Старый код (1.x)
       from aioyookassa.types import ReceiptSettlement
       
       receipt_settlement = ReceiptSettlement(
           type="prepayment",
           amount=PaymentAmount(value=100, currency="RUB")
       )
       
       # Новый код (2.0+)
       from aioyookassa.types import Settlement
       
       receipt_settlement = Settlement(
           type="prepayment",
           amount=PaymentAmount(value=100, currency="RUB")
       )

5. **Обновите вызовы API методов - теперь используются Pydantic модели**
   
   .. code-block:: python
   
       # Старый код (1.x)
       payment = await client.payments.create_payment(
           amount=PaymentAmount(value=100.00, currency=Currency.RUB),
           description="Test payment",
           confirmation=Confirmation(...),
           capture=False
       )
       
       payments = await client.payments.get_payments(
           created_at=datetime.now(),
           status=PaymentStatus.SUCCEEDED,
           limit=10
       )
       
       # Новый код (2.0+)
       from aioyookassa.types.params import CreatePaymentParams, GetPaymentsParams
       
       # Создание платежа
       params = CreatePaymentParams(
           amount=PaymentAmount(value=100.00, currency=Currency.RUB),
           description="Test payment",
           confirmation=Confirmation(...),
           capture=False
       )
       payment = await client.payments.create_payment(params)
       
       # Получение списка платежей
       params = GetPaymentsParams(
           created_at=datetime.now(),
           status=PaymentStatus.SUCCEEDED,
           limit=10
       )
       payments = await client.payments.get_payments(params)
       
       # Также поддерживается dict для обратной совместимости
       payment = await client.payments.create_payment({
           "amount": {"value": 100.00, "currency": "RUB"},
           "description": "Test payment"
       })

Полный пример миграции
'''''''''''''''''''''''

**Старый код (1.x):**
.. code-block:: python

    from aioyookassa.types import (
        RefundCancellationDetails,
        RefundSettlement,
        ReceiptSettlement
    )
    from aioyookassa.types.enum import CancellationParty, CancellationReason
    from aioyookassa.types.payment import PaymentAmount, Confirmation
    from aioyookassa.types.enum import ConfirmationType, Currency
    
    # Создание платежа (множество параметров)
    payment = await client.payments.create_payment(
        amount=PaymentAmount(value=100.00, currency=Currency.RUB),
        description="Test payment",
        confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com"),
        capture=False
    )
    
    # Для возвратов
    cancellation_details = RefundCancellationDetails(
        party=CancellationParty.MERCHANT,
        reason=CancellationReason.CANCELED_BY_MERCHANT
    )
    
    refund_settlement = RefundSettlement(
        type="payout",
        amount=PaymentAmount(value=100, currency="RUB")
    )
    
    # Для чеков
    receipt_settlement = ReceiptSettlement(
        type="prepayment",
        amount=PaymentAmount(value=100, currency="RUB")
    )

**Новый код (2.0+):**
.. code-block:: python

    from aioyookassa.types import CancellationDetails, Settlement
    from aioyookassa.types.enum import CancellationParty, CancellationReason, ConfirmationType, Currency
    from aioyookassa.types.payment import PaymentAmount, Confirmation
    from aioyookassa.types.params import CreatePaymentParams
    
    # Создание платежа (Pydantic модель)
    params = CreatePaymentParams(
        amount=PaymentAmount(value=100.00, currency=Currency.RUB),
        description="Test payment",
        confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com"),
        capture=False
    )
    payment = await client.payments.create_payment(params)
    
    # Для возвратов
    cancellation_details = CancellationDetails(
        party=CancellationParty.MERCHANT,
        reason=CancellationReason.CANCELED_BY_MERCHANT
    )
    
    refund_settlement = Settlement(
        type="payout",
        amount=PaymentAmount(value=100, currency="RUB")
    )
    
    # Для чеков
    receipt_settlement = Settlement(
        type="prepayment",
        amount=PaymentAmount(value=100, currency="RUB")
    )

Проверка миграции
'''''''''''''''''

После миграции проверьте:

1. ✅ Все импорты обновлены (используются CancellationDetails и Settlement)
2. ✅ Все использования RefundCancellationDetails заменены на CancellationDetails
3. ✅ Все использования RefundSettlement заменены на Settlement
4. ✅ Все использования ReceiptSettlement заменены на Settlement
5. ✅ Все вызовы API методов обновлены для использования Pydantic моделей (CreatePaymentParams, GetPaymentsParams, и т.д.)
6. ✅ Все тесты проходят

Известные проблемы
'''''''''''''''''''

Если вы столкнулись с проблемами после миграции:

1. **ImportError для RefundCancellationDetails**: Используйте `CancellationDetails` вместо `RefundCancellationDetails`
2. **ImportError для RefundSettlement**: Используйте `Settlement` вместо `RefundSettlement`
3. **ImportError для ReceiptSettlement**: Используйте `Settlement` вместо `ReceiptSettlement`
4. **TypeError при вызове API методов**: Теперь методы принимают Pydantic модели или dict. Используйте `CreatePaymentParams`, `GetPaymentsParams`, и т.д.
5. **Ошибка "too many arguments"**: Оберните параметры в Pydantic модель (например, `CreatePaymentParams(...)`)

Получение помощи
'''''''''''''''''

Если у вас возникли проблемы с миграцией:

- Создайте issue на GitHub с тегом `migration`
- Обратитесь к разработчику в Telegram: `@masaasibaata`
- Проверьте документацию: https://aioyookassa.readthedocs.io

.. _migration-guide:

Миграция с версии 0.x на 1.0.0 ⚠️
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**⚠️ ВАЖНО: Версия 1.0.0 содержит критические изменения, несовместимые с версиями 0.x**

Пошаговое руководство по миграции
''''''''''''''''''''''''''''''''''

1. **Обновите зависимости**
   
   Убедитесь, что у вас установлены правильные версии зависимостей:
   
   .. code-block:: bash
   
       pip install aioyookassa==1.0.0
       pip install pydantic>=2.0.0
       pip install aiohttp>=3.9.0

2. **Обновите импорты**
   
   .. code-block:: python
   
       # Старый код (0.x)
       from aioyookassa.core.client import YooKassa
       
       # Новый код (1.0+)
       from aioyookassa import YooKassa

3. **Обновите доступ к API модулям**
   
   .. code-block:: python
   
       # Старый код (0.x)
       client = YooKassa('token', 12345)
       payment = await client.create_payment(...)
       payments = await client.get_payments(...)
       payment = await client.get_payment('id')
       payment = await client.capture_payment('id')
       payment = await client.cancel_payment('id')
       
       # Новый код (1.0+)
       client = YooKassa(api_key='token', shop_id=12345)
       payment = await client.payments.create_payment(...)
       payments = await client.payments.get_payments(...)
       payment = await client.payments.get_payment('id')
       payment = await client.payments.capture_payment('id')
       payment = await client.payments.cancel_payment('id')

4. **Обновите работу с датами**
   
   .. code-block:: python
   
       # Старый код (0.x)
       payments = await client.get_payments(
           created_at="2023-01-01T00:00:00.000Z"
       )
       
       # Новый код (1.0+)
       from datetime import datetime
       payments = await client.payments.get_payments(
           created_at=datetime(2023, 1, 1, 0, 0, 0)
       )

5. **Обновите работу со списками**
   
   .. code-block:: python
   
       # Старый код (0.x)
       payments = await client.get_payments()
       for payment in payments.list:
           print(payment.id)
       
       # Новый код (1.0+)
       payments = await client.payments.get_payments()
       for payment in payments.list:
           print(payment.id)

6. **Обновите обработку исключений**
   
   Структура исключений не изменилась, но рекомендуется использовать новые импорты:
   
   .. code-block:: python
   
       # Старый код (0.x)
       from aioyookassa.exceptions.base import APIError
       
       # Новый код (1.0+) - работает так же, но лучше использовать
       from aioyookassa.exceptions import APIError, NotFound, InvalidCredentials

Полный пример миграции
'''''''''''''''''''''''

**Старый код (0.x):**
.. code-block:: python

    import asyncio
    from aioyookassa.core.client import YooKassa
    from aioyookassa.types import Confirmation
    from aioyookassa.types.payment import PaymentAmount
    from aioyookassa.types.enum import ConfirmationType, Currency

    async def process_payment():
        async with YooKassa('token', 12345) as client:
            confirmation = Confirmation(type=ConfirmationType.REDIRECT, return_url='https://example.com')
            payment = await client.create_payment(
                amount=PaymentAmount(value=100, currency=Currency.RUB),
                description='Test payment',
                confirmation=confirmation
            )
            
            payments = await client.get_payments()
            for payment in payments.list:
                print(payment.id)
            
            payment_info = await client.get_payment(payment.id)
            print(payment_info.status)

**Новый код (1.0+):**
.. code-block:: python

    import asyncio
    from datetime import datetime
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount, Confirmation

    async def process_payment():
        async with YooKassa(api_key='token', shop_id=12345) as client:
            confirmation = Confirmation(
                type=ConfirmationType.REDIRECT,
                return_url='https://example.com'
            )
            payment = await client.payments.create_payment(
                amount=PaymentAmount(value=100, currency=Currency.RUB),
                description='Test payment',
                confirmation=confirmation
            )
            
            payments = await client.payments.get_payments(
                created_at=datetime.now()
            )
            for payment in payments.list:
                print(payment.id)
            
            payment_info = await client.payments.get_payment(payment.id)
            print(payment_info.status)

Проверка миграции
'''''''''''''''''

После миграции проверьте:

1. ✅ Все импорты обновлены
2. ✅ Все вызовы API используют модульный подход (client.payments.*)
3. ✅ Все даты используют datetime объекты
4. ✅ Все списки используют поле `items` вместо `list`
5. ✅ Зависимости обновлены до требуемых версий

Известные проблемы
'''''''''''''''''''

Если вы столкнулись с проблемами после миграции:

1. **Ошибка импорта**: Убедитесь, что используете `from aioyookassa import YooKassa`
2. **AttributeError на client.create_payment**: Используйте `client.payments.create_payment`
3. **Ошибка с датами**: Убедитесь, что используете datetime объекты, а не строки
4. **Ошибка с payments.items**: Используйте `payments.list` вместо `payments.items`

Получение помощи
'''''''''''''''''

Если у вас возникли проблемы с миграцией:

- Создайте issue на GitHub с тегом `migration`
- Обратитесь к разработчику в Telegram: `@masaasibaata`
- Проверьте документацию: https://aioyookassa.readthedocs.io

Совместимость
-------------

**Python версии:**
- 3.8.1+ (рекомендуется 3.9+)
- Проверено на Python 3.8.1, 3.9, 3.10, 3.11, 3.12

**Зависимости:**
- aiohttp >= 3.9.0 (обновлено с 3.8.0 в версии 1.0.0)
- pydantic >= 2.0.0 (критическое изменение с версии 1.0.0, было 1.x)

**YooKassa API:**
- Полная совместимость с YooKassa API v3
- Поддержка всех текущих методов и типов данных
- Поддержка всех API модулей (payments, refunds, receipts, invoices, payment_methods)

**Операционные системы:**
- Linux (Ubuntu, Debian, CentOS, и др.)
- macOS (10.15+)
- Windows (10+)

**Несовместимость:**
- Версии 0.x (полная несовместимость из-за breaking changes)
- Pydantic 1.x (требуется Pydantic 2.0+)
- aiohttp < 3.9.0 (требуется aiohttp >= 3.9.0)

Поддержка
---------

**Время поддержки версий:**
- Текущая версия (2.0.x): 18 месяцев
- Версия 1.x: Поддержка прекращена (критические исправления безопасности: 6 месяцев)
- Версия 0.x: Поддержка прекращена
- Критические исправления безопасности: 24 месяца для всех версий

**Политика версионирования:**
- **MAJOR версии (2.0, 3.0, и т.д.)**: Могут содержать breaking changes
- **MINOR версии (2.1, 2.2, и т.д.)**: Новые функции, обратно совместимые
- **PATCH версии (2.0.1, 2.0.2, и т.д.)**: Исправления багов, обратно совместимые

**Каналы поддержки:**
- GitHub Issues: для багов и предложений
- Telegram: @masaasibaata для вопросов
- Документация: https://aioyookassa.readthedocs.io

**Политика безопасности:**
- Критические уязвимости исправляются в течение 24 часов
- Обычные уязвимости исправляются в течение 7 дней
- Все исправления безопасности публикуются в отдельном релизе

Вклад в развитие
----------------

**Как внести вклад:**
1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

**Требования к PR:**
- Покрытие тестами не менее 90%
- Соответствие стилю кода (black, flake8)
- Обновление документации
- Добавление changelog записи

**Типы вкладов:**
- Исправление багов
- Новые функции
- Улучшение документации
- Оптимизация производительности
- Добавление примеров
