Payouts API
===========

API для работы с выплатами.

.. autoclass:: aioyookassa.core.api.payouts.PayoutsAPI
   :members:
   :show-inheritance:

Методы
------

create_payout
~~~~~~~~~~~~~

Создание новой выплаты.

.. code-block:: python

    from aioyookassa.types.params import (
        CreatePayoutParams,
        BankCardPayoutDestinationData,
        BankCardPayoutCardData
    )
    from aioyookassa.types.payment import Money
    from aioyookassa.types.enum import Currency
    
    # Выплата на банковскую карту
    params = CreatePayoutParams(
        amount=Money(value=1000.00, currency=Currency.RUB),
        payout_destination_data=BankCardPayoutDestinationData(
            card=BankCardPayoutCardData(number="5555555555554477")
        ),
        description="Выплата по договору 37"
    )
    payout = await client.payouts.create_payout(params)
    
    # Выплата через СБП
    from aioyookassa.types.params import SbpPayoutDestinationData
    
    params = CreatePayoutParams(
        amount=Money(value=1000.00, currency=Currency.RUB),
        payout_destination_data=SbpPayoutDestinationData(
            bank_id="100000000111",
            phone="79000000000"
        )
    )
    payout = await client.payouts.create_payout(params)
    
    # Выплата на кошелек ЮMoney
    from aioyookassa.types.params import YooMoneyPayoutDestinationData
    
    params = CreatePayoutParams(
        amount=Money(value=1000.00, currency=Currency.RUB),
        payout_destination_data=YooMoneyPayoutDestinationData(
            account_number="41001614575714"
        )
    )
    payout = await client.payouts.create_payout(params)

get_payout
~~~~~~~~~~

Получение информации о конкретной выплате.

.. code-block:: python

    payout = await client.payouts.get_payout("payout_id")
    print(f"Status: {payout.status}")
    print(f"Amount: {payout.amount.value} {payout.amount.currency}")

