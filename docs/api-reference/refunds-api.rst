Refunds API
===========

API для работы с возвратами.

.. autoclass:: aioyookassa.core.api.refunds.RefundsAPI
   :members:
   :show-inheritance:

Методы
------

create_refund
~~~~~~~~~~~~~

Создание нового возврата.

.. code-block:: python

    from aioyookassa.types.enum import Currency
    from aioyookassa.types.params import CreateRefundParams
    from aioyookassa.types.payment import PaymentAmount
    
    params = CreateRefundParams(
        payment_id="payment_id",
        amount=PaymentAmount(value=50.00, currency=Currency.RUB),
        description="Частичный возврат"
    )
    refund = await client.refunds.create_refund(params)

get_refunds
~~~~~~~~~~~

Получение списка возвратов с возможностью фильтрации.

.. code-block:: python

    from aioyookassa.types.params import GetRefundsParams
    
    params = GetRefundsParams(
        payment_id="payment_id",
        status="succeeded",
        limit=10
    )
    refunds = await client.refunds.get_refunds(params)

get_refund
~~~~~~~~~~

Получение информации о конкретном возврате.

.. code-block:: python

    refund = await client.refunds.get_refund("refund_id")

