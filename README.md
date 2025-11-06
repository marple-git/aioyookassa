[![Downloads](https://pepy.tech/badge/aioyookassa)](https://pepy.tech/project/aioyookassa)
[![Downloads](https://pepy.tech/badge/aioyookassa/month)](https://pepy.tech/project/aioyookassa)
[![Downloads](https://pepy.tech/badge/aioyookassa/week)](https://pepy.tech/project/aioyookassa)

![Social Preview](.github/social-preview.png)

# aioyookassa

**Асинхронная Python библиотека для работы с API YooKassa**

`aioyookassa` — это современная асинхронная библиотека для интеграции с платежным сервисом YooKassa. Библиотека предоставляет удобный интерфейс для работы с платежами, возвратами, чеками и другими функциями YooKassa API.

## ✨ Особенности

- 🚀 **Асинхронность** — полная поддержка `asyncio` для высокопроизводительных приложений
- 🛡️ **Типизация** — полная поддержка типов с использованием Pydantic моделей
- 🔧 **Простота** — интуитивно понятный API для быстрой интеграции
- 📚 **Документация** — подробная документация с примерами использования
- 🧪 **Тестирование** — 90% покрытие кода тестами
- ⚡ **Производительность** — оптимизированная работа с HTTP запросами

## 🔗 Links

- 🎓 **Documentation:** [_CLICK_](https://aioyookassa.readthedocs.io/en/latest/)
- 🖱️ **Developer contacts:** [![Dev-Telegram](https://img.shields.io/badge/Telegram-blue.svg?style=flat-square&logo=telegram)](https://t.me/masaasibaata)
- 💝 **Support project:** [![Tribute](https://img.shields.io/badge/Support%20Project-Tribute-green.svg?style=flat-square&logo=telegram)](https://t.me/tribute/app?startapp=dzqR)

## 🐦 Dependencies

| Library  |                       Description                       |
| :------: | :-----------------------------------------------------: |
| aiohttp  | Asynchronous HTTP Client/Server for asyncio and Python. |
| pydantic |                   JSON Data Validator                   |

## 📁 Project Structure

```
aioyookassa/
├── core/                    # Core functionality
│   ├── client.py           # Main YooKassa client
│   ├── api/                # API client implementations
│   │   ├── payments.py     # Payment operations
│   │   ├── receipts.py     # Fiscal receipt operations
│   │   ├── invoices.py     # Invoice operations
│   │   ├── refunds.py      # Refund operations
│   │   └── payment_methods.py # Payment method management
│   ├── methods/            # API method definitions
│   └── abc/                # Abstract base classes
├── types/                  # Pydantic models and enums
├── exceptions/             # Custom exceptions
└── __init__.py            # Package exports
```

## 🚀 Quick Start

### Установка

```bash
pip install aioyookassa
```

### Базовое использование

```python
import asyncio
from datetime import datetime
from aioyookassa import YooKassa
from aioyookassa.types.payment import PaymentAmount, Confirmation
from aioyookassa.types.enum import PaymentStatus, ConfirmationType, Currency

async def main():
    # Инициализация клиента
    client = YooKassa(api_key="your_api_key", shop_id=12345)

    # Создание платежа
    payment = await client.payments.create_payment(
        amount=PaymentAmount(value=100.00, currency=Currency.RUB),
        confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com/return"),
        description="Тестовый платеж"
    )

    print(f"Payment created: {payment.id}")
    print(f"Confirmation URL: {payment.confirmation.confirmation_url}")

    # Получение информации о платеже
    payment_info = await client.payments.get_payment(payment.id)
    print(f"Payment status: {payment_info.status}")

    # Получение списка платежей за сегодня
    today = datetime.now()
    payments = await client.payments.get_payments(
        created_at=today,
        status=PaymentStatus.SUCCEEDED
    )
    print(f"Found {len(payments.list)} successful payments today")

    # Закрытие клиента
    await client.close()

# Запуск
asyncio.run(main())
```

## 📋 Основные методы

### 💳 Платежи (Payments)

```python
from datetime import datetime
from aioyookassa.types.enum import PaymentStatus, ConfirmationType, Currency

# Создание платежа
payment = await client.payments.create_payment(
    amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
    confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com/return"),
    description="Оплата заказа #12345"
)

# Получение списка платежей
payments = await client.payments.get_payments(
    created_at=datetime(2023, 1, 1, 12, 0, 0),
    status=PaymentStatus.SUCCEEDED,
    limit=10
)

# Получение конкретного платежа
payment = await client.payments.get_payment("payment_id")

# Подтверждение платежа
await client.payments.capture_payment("payment_id")

# Отмена платежа
await client.payments.cancel_payment("payment_id")
```

### 💰 Возвраты (Refunds)

```python
# Создание возврата
refund = await client.refunds.create_refund(
    payment_id="payment_id",
    amount=PaymentAmount(value=500.00, currency=Currency.RUB),
    description="Частичный возврат"
)

# Получение информации о возврате
refund_info = await client.refunds.get_refund("refund_id")
```

### 🧾 Чеки (Receipts)

```python
from aioyookassa.types.payment import PaymentItem
from aioyookassa.types.enum import PaymentSubject, PaymentMode

# Регистрация чека
receipt = await client.receipts.create_receipt(
    payment_id="payment_id",
    items=[
        PaymentItem(
            description="Товар",
            quantity=1,
            amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
            vat_code=1,
            payment_subject=PaymentSubject.COMMODITY,
            payment_mode=PaymentMode.FULL_PAYMENT
        )
    ],
    tax_system_code=1
)

# Получение информации о чеке
receipt_info = await client.receipts.get_receipt("receipt_id")
```

### 📄 Счета (Invoices)

```python
# Создание счета
invoice = await client.invoices.create_invoice(
    amount=PaymentAmount(value=2000.00, currency=Currency.RUB),
    description="Счет на оплату"
)

# Получение информации о счете
invoice_info = await client.invoices.get_invoice("invoice_id")
```

## 🔧 Контекстный менеджер

```python
from datetime import datetime
from aioyookassa.types.enum import PaymentStatus, ConfirmationType, Currency

async with YooKassa(api_key="your_key", shop_id=12345) as client:
    payment = await client.payments.create_payment(
        amount=PaymentAmount(value=100.00, currency=Currency.RUB),
        confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com/return")
    )

    # Получение платежей за последний час
    recent_payments = await client.payments.get_payments(
        created_at=datetime.now(),
        status=PaymentStatus.SUCCEEDED,
        limit=5
    )
    # Клиент автоматически закроется
```

## 🛠️ Установка и настройка

### Требования

- Python 3.8.1+
- aiohttp
- pydantic

### Установка через pip

```bash
pip install aioyookassa
```

### Установка через Poetry

```bash
poetry add aioyookassa
```

## 📖 Документация

Полная документация доступна по адресу: [aioyookassa.readthedocs.io](https://aioyookassa.readthedocs.io/en/latest/)

## 🤝 Поддержка проекта

Если библиотека оказалась полезной, вы можете поддержать проект:

- 💝 **[Tribute](https://t.me/tribute/app?startapp=dzqR)** — поддержка через Telegram
- 🐛 **Сообщить об ошибке** — [GitHub Issues](https://github.com/masasibata/aioyookassa/issues)
- 💬 **Связаться с разработчиком** — [@masaasibaata](https://t.me/masaasibaata)

## 🚀 Вклад в развитие

Мы приветствуем вклад в развитие библиотеки! Вот как вы можете помочь:

### Быстрый старт для разработчиков

```bash
# Клонирование репозитория
git clone https://github.com/masasibata/aioyookassa.git
cd aioyookassa

# Установка зависимостей для разработки
make install-dev

# Установка pre-commit хуков
make pre-commit

# Запуск всех проверок
make all-checks
```

### Доступные команды

```bash
# Тестирование
make test                 # Запуск тестов
make test-cov            # Тесты с покрытием кода
make test-fast           # Быстрые тесты без покрытия

# Качество кода
make lint                # Линтинг (Black)
make format              # Форматирование кода
make type-check          # Проверка типов (MyPy)
make all-checks          # Все проверки качества

# Сборка и публикация
make build               # Сборка пакета
make clean               # Очистка артефактов

# Документация
make docs                # Сборка документации
make docs-serve          # Локальный сервер документации

# Локальная разработка
make dev                 # Запуск пайплайна разработки локально
```

### Процесс внесения изменений

1. **Форкните репозиторий** на GitHub
2. **Создайте ветку** для ваших изменений:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Внесите изменения** и убедитесь, что все проверки проходят:
   ```bash
   make all-checks
   ```
4. **Зафиксируйте изменения**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```
5. **Отправьте изменения**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Создайте Pull Request** на GitHub

### Требования к Pull Request

- ✅ **Все тесты проходят** (`make test`)
- ✅ **Покрытие кода не менее 90%** (`make test-cov`)
- ✅ **Код отформатирован** (`make format`)
- ✅ **Форматирование проходит** (`make lint`)
- ✅ **Проверка типов проходит** (`make type-check`)
- ✅ **Документация обновлена** (если необходимо)
- ✅ **Описательное сообщение коммита**

### Типы вкладов

- 🐛 **Исправление багов** — исправление ошибок в коде
- ✨ **Новые функции** — добавление новой функциональности
- 📚 **Документация** — улучшение документации и примеров
- ⚡ **Оптимизация** — улучшение производительности
- 🧪 **Тесты** — добавление или улучшение тестов
- 🔧 **Инфраструктура** — улучшение инструментов разработки

### Соглашения о коммитах

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add new payment method support
fix: resolve timeout issue in payment creation
docs: update API documentation
test: add tests for refund functionality
refactor: improve error handling
```

### Получение помощи

- 💬 **Вопросы** — [@masaasibaata](https://t.me/masaasibaata)
- 🐛 **Проблемы** — [GitHub Issues](https://github.com/masasibata/aioyookassa/issues)

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

---
