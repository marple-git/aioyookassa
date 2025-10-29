Contributing
============

Спасибо за интерес к проекту aioyookassa! Ваш вклад поможет сделать библиотеку лучше.

Как внести вклад
----------------

Сообщение об ошибках
~~~~~~~~~~~~~~~~~~~~

**Перед созданием issue:**
1. Проверьте, что ошибка не была уже сообщена
2. Убедитесь, что используете последнюю версию
3. Проверьте документацию

**Создание issue:**
1. Перейдите в `GitHub Issues <https://github.com/your-repo/aioyookassa/issues>`_
2. Выберите шаблон "Bug Report"
3. Заполните все необходимые поля

**Шаблон для бага:**

.. code-block:: text

    **Описание бага**
    Краткое описание проблемы.

    **Шаги для воспроизведения**
    1. Перейдите к '...'
    2. Нажмите на '...'
    3. Прокрутите до '...'
    4. Увидите ошибку

    **Ожидаемое поведение**
    Что должно было произойти.

    **Фактическое поведение**
    Что произошло на самом деле.

    **Скриншоты**
    Если применимо, добавьте скриншоты.

    **Окружение:**
    - OS: [e.g. Ubuntu 20.04]
    - Python: [e.g. 3.9.7]
    - aioyookassa: [e.g. 0.1.6]

    **Дополнительный контекст**
    Любая другая информация о проблеме.

Предложения функций
~~~~~~~~~~~~~~~~~~~

**Создание feature request:**
1. Перейдите в `GitHub Issues <https://github.com/your-repo/aioyookassa/issues>`_
2. Выберите шаблон "Feature Request"
3. Опишите предлагаемую функцию

**Шаблон для предложения:**

.. code-block:: text

    **Описание функции**
    Краткое описание предлагаемой функции.

    **Проблема, которую решает**
    Какая проблема решается этой функцией?

    **Предлагаемое решение**
    Опишите, как должна работать функция.

    **Альтернативы**
    Рассматривали ли вы альтернативные решения?

    **Дополнительный контекст**
    Любая другая информация о предложении.

Разработка
----------

Настройка окружения
~~~~~~~~~~~~~~~~~~~

1. **Форкните репозиторий:**
   - Перейдите на `GitHub <https://github.com/your-repo/aioyookassa>`_
   - Нажмите "Fork"

2. **Клонируйте форк:**
   .. code-block:: bash

       git clone https://github.com/your-username/aioyookassa.git
       cd aioyookassa

3. **Установите зависимости:**
   .. code-block:: bash

       # Используя Poetry (рекомендуется)
       poetry install

       # Или используя pip
       pip install -e ".[dev]"

4. **Установите pre-commit хуки:**
   .. code-block:: bash

       pre-commit install

Структура проекта
~~~~~~~~~~~~~~~~~

.. code-block:: text

    aioyookassa/
    ├── aioyookassa/           # Основной код библиотеки
    │   ├── core/             # Ядро библиотеки
    │   ├── types/            # Pydantic модели
    │   ├── exceptions/       # Исключения
    │   └── __init__.py
    ├── tests/                # Тесты
    ├── docs/                 # Документация
    ├── examples/             # Примеры использования
    ├── pyproject.toml        # Конфигурация Poetry
    ├── pytest.ini           # Конфигурация pytest
    └── README.md

Создание Pull Request
~~~~~~~~~~~~~~~~~~~~~

1. **Создайте ветку:**
   .. code-block:: bash

       git checkout -b feature/your-feature-name
       # или
       git checkout -b fix/your-bug-fix

2. **Внесите изменения:**
   - Реализуйте функцию или исправьте баг
   - Добавьте тесты
   - Обновите документацию

3. **Запустите тесты:**
   .. code-block:: bash

       # Все тесты
       poetry run pytest

       # С покрытием
       poetry run pytest --cov=aioyookassa --cov-report=html

       # Конкретный тест
       poetry run pytest tests/core/test_client.py::TestYooKassa::test_yookassa_initialization

4. **Проверьте код:**
   .. code-block:: bash

       # Форматирование
       poetry run black aioyookassa tests

       # Линтинг
       poetry run flake8 aioyookassa tests

       # Типы
       poetry run mypy aioyookassa

5. **Закоммитьте изменения:**
   .. code-block:: bash

       git add .
       git commit -m "feat: add new feature"
       # или
       git commit -m "fix: resolve bug in payment processing"

6. **Отправьте PR:**
   .. code-block:: bash

       git push origin feature/your-feature-name

Стандарты кода
--------------

Форматирование
~~~~~~~~~~~~~~

Используем **Black** для форматирования:

.. code-block:: bash

    poetry run black aioyookassa tests

**Настройки Black:**
- Длина строки: 88 символов
- Кавычки: двойные
- Отступы: 4 пробела

Линтинг
~~~~~~~

Используем **Flake8** для проверки стиля:

.. code-block:: bash

    poetry run flake8 aioyookassa tests

**Настройки Flake8:**
- Максимальная длина строки: 88
- Максимальная сложность: 10
- Игнорируем: E203, W503

Типизация
~~~~~~~~~

Используем **mypy** для проверки типов:

.. code-block:: bash

    poetry run mypy aioyookassa

**Требования:**
- Все публичные функции должны иметь аннотации типов
- Используйте `typing` модуль для сложных типов
- Избегайте `Any` где это возможно

Документация
~~~~~~~~~~~~

**Docstrings:**
Используйте Google стиль:

.. code-block:: python

    def create_payment(self, amount: PaymentAmount, description: str) -> Payment:
        """
        Создание нового платежа.

        Args:
            amount: Сумма платежа
            description: Описание платежа

        Returns:
            Созданный платеж

        Raises:
            APIError: При ошибке API
            InvalidRequestError: При неверном запросе

        Example:
            >>> from aioyookassa.types.enum import Currency
            >>> payment = await client.payments.create_payment(
            ...     amount=PaymentAmount(value=100, currency=Currency.RUB),
            ...     description="Test payment"
            ... )
        """
        pass

**Комментарии:**
- Объясняйте сложную логику
- Избегайте очевидных комментариев
- Используйте русский язык для комментариев

Тестирование
------------

Структура тестов
~~~~~~~~~~~~~~~~

.. code-block:: text

    tests/
    ├── conftest.py              # Общие фикстуры
    ├── core/                    # Тесты core модулей
    ├── types/                   # Тесты типов данных
    ├── exceptions/              # Тесты исключений
    └── fixtures/                # Тестовые данные

Покрытие кода
~~~~~~~~~~~~~

**Требования:**
- Минимальное покрытие: 90%
- Новые функции: 100% покрытие
- Критический код: 100% покрытие

**Проверка покрытия:**
.. code-block:: bash

    poetry run pytest --cov=aioyookassa --cov-report=html --cov-report=term-missing

**Исключения из покрытия:**
- `if __name__ == "__main__":` блоки
- Исключения в тестах
- Документационные примеры

Типы тестов
~~~~~~~~~~~

**Unit тесты:**
- Тестируют отдельные функции/методы
- Изолированы от внешних зависимостей
- Быстрые (< 1ms)

**Integration тесты:**
- Тестируют взаимодействие компонентов
- Могут использовать моки
- Средняя скорость (< 100ms)

**Пример unit теста:**
.. code-block:: python

    import pytest
    from aioyookassa.types.payment import PaymentAmount
    from aioyookassa.types.enum import Currency

    def test_payment_amount_creation():
        """Test PaymentAmount creation with valid data."""
        amount = PaymentAmount(value=100.50, currency=Currency.RUB)
        
        assert amount.value == 100.50
        assert amount.currency == Currency.RUB

**Пример integration теста:**
.. code-block:: python

    import pytest
    from unittest.mock import AsyncMock, patch
    from aioyookassa import YooKassa

    @pytest.mark.asyncio
    async def test_create_payment_integration():
        """Test payment creation with mocked API."""
        with patch('aioyookassa.core.api.payments.PaymentsAPI.create_payment') as mock_create:
            mock_create.return_value = AsyncMock()
            mock_create.return_value.id = "test_payment_id"
            
            from aioyookassa.types.enum import Currency
            
            client = YooKassa(api_key="test", shop_id=12345)
            payment = await client.payments.create_payment(
                amount=PaymentAmount(value=100, currency=Currency.RUB),
                description="Test"
            )
            
            assert payment.id == "test_payment_id"
            mock_create.assert_called_once()

Фикстуры
~~~~~~~~

**Общие фикстуры в conftest.py:**
.. code-block:: python

    import pytest
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount

    @pytest.fixture
    def client():
        """Test client fixture."""
        return YooKassa(api_key="test_key", shop_id=12345)

    @pytest.fixture
    def sample_payment_data():
        """Sample payment data for tests."""
        return {
            "id": "test_payment_id",
            "status": "succeeded",
            "amount": {"value": "100.00", "currency": "RUB"},
            "description": "Test payment"
        }

Релизный процесс
----------------

Версионирование
~~~~~~~~~~~~~~~

Используем `Semantic Versioning <https://semver.org/>`_:

- **MAJOR**: Несовместимые изменения API
- **MINOR**: Новая функциональность (обратно совместимая)
- **PATCH**: Исправления багов (обратно совместимые)

**Примеры:**
- `1.0.0` → `1.0.1` (исправление бага)
- `1.0.1` → `1.1.0` (новая функция)
- `1.1.0` → `2.0.0` (breaking change)

Подготовка релиза
~~~~~~~~~~~~~~~~~

1. **Обновите версию:**
   - В `pyproject.toml`
   - В `docs/conf.py`
   - В `aioyookassa/__init__.py`

2. **Обновите changelog:**
   - Добавьте записи в `docs/changelog.rst`
   - Опишите все изменения

3. **Запустите тесты:**
   .. code-block:: bash

       poetry run pytest
       poetry run black aioyookassa tests
       poetry run flake8 aioyookassa tests
       poetry run mypy aioyookassa

4. **Создайте тег:**
   .. code-block:: bash

       git tag v0.1.7
       git push origin v0.1.7

5. **Создайте релиз на GitHub:**
   - Перейдите в Releases
   - Нажмите "Create a new release"
   - Выберите тег
   - Заполните описание

Публикация
~~~~~~~~~~

**PyPI:**
.. code-block:: bash

    poetry build
    poetry publish

**GitHub:**
- Автоматически через GitHub Actions
- При создании тега

Кодекс поведения
----------------

Наши обязательства
~~~~~~~~~~~~~~~~~~

Мы обязуемся сделать участие в нашем проекте комфортным для всех, независимо от:

- Возраста
- Размера тела
- Инвалидности
- Этнической принадлежности
- Половых характеристик
- Гендерной идентичности и выражения
- Уровня опыта
- Образования
- Социально-экономического статуса
- Национальности
- Внешности
- Расы
- Религии
- Сексуальной идентичности и ориентации

Наши стандарты
~~~~~~~~~~~~~~

**Примеры поведения, которое способствует созданию позитивной среды:**

- Использование доброжелательного и инклюзивного языка
- Уважение к различным точкам зрения и опыту
- Принятие конструктивной критики
- Фокус на том, что лучше для сообщества
- Проявление эмпатии к другим участникам сообщества

**Примеры неприемлемого поведения:**

- Использование сексуализированного языка или образов
- Троллинг, оскорбительные/уничижительные комментарии
- Публичные или частные домогательства
- Публикация личной информации без разрешения
- Другое поведение, которое может считаться неуместным в профессиональной среде

Применение
~~~~~~~~~~

Случаи оскорбительного, домогательского или иного неприемлемого поведения могут быть сообщены, обратившись к ответственному за проект по адресу masaasibaata@telegram.

Все жалобы будут рассмотрены и расследованы, и приведут к ответу, который считается необходимым и соответствующим обстоятельствам.

Контакты
--------

**Основной разработчик:**
- Telegram: `@masaasibaata <https://t.me/masaasibaata>`_

**Поддержка проекта:**
- `Tribute <https://t.me/tribute/app?startapp=dzqR>`_

**Репозиторий:**
- `GitHub <https://github.com/your-repo/aioyookassa>`_

**Документация:**
- `Read the Docs <https://aioyookassa.readthedocs.io>`_

**Пакет:**
- `PyPI <https://pypi.org/project/aioyookassa/>`_

