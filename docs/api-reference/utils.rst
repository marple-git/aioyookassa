Утилиты
=======

Вспомогательные функции для работы с API.

.. automodule:: aioyookassa.core.utils
   :members:
   :undoc-members:
   :show-inheritance:

Примеры использования
---------------------

Генерация ключа идемпотентности
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.core.utils import generate_idempotence_key, create_idempotence_headers

    # Генерация ключа
    key = generate_idempotence_key()
    print(key)  # "550e8400-e29b-41d4-a716-446655440000"

    # Создание заголовков
    headers = create_idempotence_headers()
    # {"Idempotence-Key": "550e8400-e29b-41d4-a716-446655440000"}

Удаление None значений
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.core.utils import remove_none_values

    # Удаление None значений из словаря
    params = {
        "amount": 100.0,
        "description": "Test payment",
        "metadata": None,
        "receipt": None,
    }

    cleaned = remove_none_values(params)
    # {"amount": 100.0, "description": "Test payment"}

Нормализация параметров
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa.core.utils import normalize_params
    from aioyookassa.types.params import CreatePaymentParams

    # Нормализация из Pydantic модели
    params = CreatePaymentParams(amount=PaymentAmount(...), description="Test")
    normalized = normalize_params(params)
    # {"amount": {...}, "description": "Test"}

    # Нормализация из словаря
    params_dict = {"amount": {...}, "description": "Test"}
    normalized = normalize_params(params_dict, CreatePaymentParams)
    # Валидированный и нормализованный словарь

Форматирование дат
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import datetime
    from aioyookassa.core.utils import format_datetime_to_iso, format_datetime_params

    # Форматирование одной даты
    dt = datetime(2024, 1, 1, 12, 0, 0)
    iso_string = format_datetime_to_iso(dt)
    # "2024-01-01T12:00:00"

    # Форматирование нескольких полей
    params = {
        "created_at": datetime(2024, 1, 1),
        "expires_at": datetime(2024, 12, 31),
        "other_field": "value",
    }
    formatted = format_datetime_params(
        params, ["created_at", "expires_at"]
    )
    # {"created_at": "2024-01-01T00:00:00", "expires_at": "2024-12-31T00:00:00", "other_field": "value"}

