Receipts API
============

API для работы с фискальными чеками.

.. autoclass:: aioyookassa.core.api.receipts.ReceiptsAPI
   :members:
   :show-inheritance:

Методы
------

create_receipt
~~~~~~~~~~~~~~

Создание нового чека.

.. code-block:: python

    from aioyookassa.types.params import CreateReceiptParams
    from aioyookassa.types.enum import ReceiptType, Currency
    from aioyookassa.types.payment import PaymentItem, PaymentAmount, PaymentSubject, PaymentMode
    from aioyookassa.types.payment import Settlement
    
    params = CreateReceiptParams(
        type=ReceiptType.PAYMENT,
        payment_id="payment_id",
        items=[
            PaymentItem(
                description="Товар",
                quantity=1,
                amount=PaymentAmount(value=100.00, currency=Currency.RUB),
                vat_code=1,
                payment_subject=PaymentSubject.COMMODITY,
                payment_mode=PaymentMode.FULL_PAYMENT
            )
        ],
        settlements=[
            Settlement(
                type="prepayment",
                amount=PaymentAmount(value=100.00, currency=Currency.RUB)
            )
        ],
        tax_system_code=1
    )
    receipt = await client.receipts.create_receipt(params)

get_receipts
~~~~~~~~~~~~

Получение списка чеков с возможностью фильтрации.

.. code-block:: python

    from aioyookassa.types.params import GetReceiptsParams
    from aioyookassa.types.enum import ReceiptStatus
    
    params = GetReceiptsParams(
        payment_id="payment_id",
        status=ReceiptStatus.SUCCEEDED,
        limit=10
    )
    receipts = await client.receipts.get_receipts(params)

get_receipt
~~~~~~~~~~~

Получение информации о конкретном чеке.

.. code-block:: python

    receipt = await client.receipts.get_receipt("receipt_id")

