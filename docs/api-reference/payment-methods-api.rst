Payment Methods API
===================

API для работы со способами оплаты.

.. autoclass:: aioyookassa.core.api.payment_methods.PaymentMethodsAPI
   :members:
   :show-inheritance:

Методы
------

create_payment_method
~~~~~~~~~~~~~~~~~~~~~~

Создание нового способа оплаты.

.. code-block:: python

    from aioyookassa.types.params import (
        CreatePaymentMethodParams,
        PaymentMethodCardData,
        PaymentMethodHolder,
        PaymentMethodConfirmation
    )
    
    params = CreatePaymentMethodParams(
        type="bank_card",
        card=PaymentMethodCardData(
            number="5555555555554444",
            expiry_year="2025",
            expiry_month="12",
            cardholder="John Doe",
            csc="123"
        ),
        holder=PaymentMethodHolder(
            gateway_id="gateway_123",
            client_ip="192.168.1.1"
        ),
        confirmation=PaymentMethodConfirmation(
            type="redirect",
            return_url="https://example.com/return"
        )
    )
    payment_method = await client.payment_methods.create_payment_method(params)

get_payment_method
~~~~~~~~~~~~~~~~~~

Получение информации о конкретном способе оплаты.

.. code-block:: python

    payment_method = await client.payment_methods.get_payment_method("payment_method_id")

