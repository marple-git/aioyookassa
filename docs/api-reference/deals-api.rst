Deals API
=========

API для работы с безопасными сделками.

.. autoclass:: aioyookassa.core.api.deals.DealsAPI
   :members:
   :show-inheritance:

Методы
------

create_deal
~~~~~~~~~~~

Создание новой сделки.

.. code-block:: python

    from aioyookassa.types.params import CreateDealParams
    from aioyookassa.types.enum import FeeMoment
    
    params = CreateDealParams(
        type="safe_deal",
        fee_moment=FeeMoment.PAYMENT_SUCCEEDED,  # или FeeMoment.DEAL_CLOSED
        description="Безопасная сделка для продажи товара",
        metadata={"order_id": "12345"}
    )
    deal = await client.deals.create_deal(params)

get_deals
~~~~~~~~~

Получение списка сделок с возможностью фильтрации.

.. code-block:: python

    from aioyookassa.types.params import GetDealsParams
    from datetime import datetime
    from aioyookassa.types.enum import DealStatus
    
    # Получение всех сделок
    deals = await client.deals.get_deals()
    
    # С фильтрацией
    params = GetDealsParams(
        created_at_gte=datetime(2024, 1, 1),
        status=DealStatus.OPENED,
        limit=10
    )
    deals = await client.deals.get_deals(params)
    
    if deals.list:
        for deal in deals.list:
            print(f"Deal {deal.id}: {deal.status}, Balance: {deal.balance.value}")

get_deal
~~~~~~~~

Получение информации о конкретной сделке.

.. code-block:: python

    deal = await client.deals.get_deal("deal_id")
    print(f"Status: {deal.status}")
    print(f"Balance: {deal.balance.value} {deal.balance.currency}")
    print(f"Payout balance: {deal.payout_balance.value} {deal.payout_balance.currency}")

