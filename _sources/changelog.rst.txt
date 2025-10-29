Changelog
=========

История изменений aioyookassa.

Версия 1.0.0 (Текущая) ⚠️ BREAKING CHANGES
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

Версия 1.1.0 (Планируется)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Новые возможности:**
- Добавление поддержки webhook'ов для обработки уведомлений
- Расширенная система логирования с возможностью кастомизации
- Метрики и мониторинг интеграции
- Кэширование ответов API для улучшения производительности
- Поддержка batch операций для массовых операций

**Улучшения:**
- Оптимизация производительности
- Расширенная документация с дополнительными примерами
- Дополнительные примеры интеграции с популярными фреймворками

**Технические улучшения:**
- Поддержка retry механизмов для автоматических повторов запросов
- Улучшенная обработка таймаутов
- Расширенная система конфигурации

Версия 1.2.0 (Планируется)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Новые возможности:**
- Интеграция с популярными фреймворками (FastAPI, Django)
- CLI инструменты для управления
- Расширенная система плагинов
- Поддержка middleware для кастомизации запросов

**Улучшения:**
- Автоматическое масштабирование
- Продвинутые метрики
- Интеграция с системами мониторинга (Prometheus, Grafana)

Версия 2.0.0 (Долгосрочные планы)
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

    async def process_payment():
        async with YooKassa('token', 12345) as client:
            confirmation = Confirmation(type='redirect', return_url='https://example.com')
            payment = await client.create_payment(
                amount=PaymentAmount(value=100, currency='RUB'),
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
                type='redirect',
                return_url='https://example.com'
            )
            payment = await client.payments.create_payment(
                amount=PaymentAmount(value=100, currency='RUB'),
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
- Текущая версия (1.0.x): 18 месяцев
- Версия 0.x: Поддержка прекращена (критические исправления безопасности: 6 месяцев)
- Критические исправления безопасности: 24 месяца для всех версий

**Политика версионирования:**
- **MAJOR версии (1.0, 2.0, и т.д.)**: Могут содержать breaking changes
- **MINOR версии (1.1, 1.2, и т.д.)**: Новые функции, обратно совместимые
- **PATCH версии (1.0.1, 1.0.2, и т.д.)**: Исправления багов, обратно совместимые

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
