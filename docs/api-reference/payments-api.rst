Payments API
============

API для работы с платежами.

.. autoclass:: aioyookassa.core.api.payments.PaymentsAPI
   :members:
   :show-inheritance:

Методы
------

create_payment
~~~~~~~~~~~~~~

Создание нового платежа.

.. code-block:: python

    payment = await client.payments.create_payment(
        amount=PaymentAmount(value=100.00, currency="RUB"),
        confirmation=Confirmation(type="redirect", return_url="https://example.com/return"),
        description="Тестовый платеж"
    )

get_payments
~~~~~~~~~~~~

Получение списка платежей с возможностью фильтрации.

.. code-block:: python

    from datetime import datetime
    from aioyookassa.types.enum import PaymentStatus

    payments = await client.payments.get_payments(
        created_at=datetime(2023, 1, 1, 12, 0, 0),
        status=PaymentStatus.SUCCEEDED,
        limit=10
    )

get_payment
~~~~~~~~~~~

Получение информации о конкретном платеже.

.. code-block:: python

    payment = await client.payments.get_payment("payment_id")

capture_payment
~~~~~~~~~~~~~~~

Подтверждение платежа.

.. code-block:: python

    payment = await client.payments.capture_payment("payment_id")

cancel_payment
~~~~~~~~~~~~~~

Отмена платежа.

.. code-block:: python

    payment = await client.payments.cancel_payment("payment_id")

