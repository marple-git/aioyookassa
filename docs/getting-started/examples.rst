Payments
============


How to create a payment?
----------------------------


.. code-block:: python

    import asyncio

    from aioyookassa.core.client import YooKassa
    from aioyookassa.types import Confirmation
    from aioyookassa.types.payment import PaymentAmount


    async def create_payment():
        async with YooKassa('token', 99999) as client:
            confirmation = Confirmation(type='redirect', return_url='https://example.com')
            payment = await client.create_payment(amount=PaymentAmount(value=100, currency='RUB'),
                                                  description='Test payment', confirmation=confirmation)
            print(payment.confirmation.url) # Payment URL

    asyncio.run(create_payment())

How to get payments?
-------------------------


.. code-block:: python

    import asyncio

    from aioyookassa.core.client import YooKassa


    async def get_payments():
        async with YooKassa('token', 99999) as client:
            payments = await client.get_payments()
            for payment in payments.list:
                print(payment.amount)  # value=100.0 currency='RUB'


    asyncio.run(get_payments())

How to get one single payment?
-------------------------------


.. code-block:: python

    import asyncio

    from aioyookassa.core.client import YooKassa


    async def get_payment():
        async with YooKassa('token', 99999) as client:
            payment = await client.get_payment('PAYMENT_ID')
            print(payment.confirmation.url)  # Payment URL


    asyncio.run(get_payment())



How to capture a payment?
---------------------------------


.. code-block:: python

    import asyncio

    from aioyookassa.core.client import YooKassa


    async def capture_payment():
        async with YooKassa('token', 99999) as client:
            payment = await client.capture_payment('payment_id')
            print(payment.confirmation.url)  # Payment URL


    asyncio.run(capture_payment())

How to cancel payment?
------------------------


.. code-block:: python

    import asyncio

    from aioyookassa.core.client import YooKassa


    async def cancel_payment():
        async with YooKassa('token', 999999) as client:
            payment = await client.capture_payment('payment_id')
            print(payment.confirmation.url)  # Payment URL


    asyncio.run(cancel_payment())
