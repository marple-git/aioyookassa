Invoices API
============

API для работы со счетами на оплату.

.. autoclass:: aioyookassa.core.api.invoices.InvoicesAPI
   :members:
   :show-inheritance:

Методы
------

create_invoice
~~~~~~~~~~~~~~

Создание нового счета.

.. code-block:: python

    from datetime import datetime, timedelta
    from aioyookassa.types.params import CreateInvoiceParams
    from aioyookassa.types.payment import PaymentAmount
    from aioyookassa.types.enum import Currency
    from aioyookassa.types.invoice import InvoicePaymentData, InvoiceCartItem
    
    params = CreateInvoiceParams(
        payment_data=InvoicePaymentData(
            type="bank_card",
            account_id="123456789"
        ),
        cart=[
            InvoiceCartItem(
                description="Услуга",
                quantity=1,
                amount=PaymentAmount(value=1000.00, currency=Currency.RUB),
                vat_code=1
            )
        ],
        expires_at=datetime.now() + timedelta(days=7),
        description="Счет на оплату"
    )
    invoice = await client.invoices.create_invoice(params)

get_invoice
~~~~~~~~~~~

Получение информации о конкретном счете.

.. code-block:: python

    invoice = await client.invoices.get_invoice("invoice_id")

