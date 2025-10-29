YooKassa Client
===============

Основной клиент для работы с API YooKassa.

.. autoclass:: aioyookassa.core.client.YooKassa
   :members:
   :special-members: __init__, __aenter__, __aexit__
   :show-inheritance:

Примеры использования
---------------------

Инициализация клиента
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from aioyookassa import YooKassa

    # С API ключом и ID магазина
    client = YooKassa(api_key="your_api_key", shop_id=12345)
    
    # С строковым ID магазина
    client = YooKassa(api_key="your_api_key", shop_id="12345")

Использование контекстного менеджера
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    async with YooKassa(api_key="your_key", shop_id=12345) as client:
        # Работа с API
        payment = await client.payments.create_payment(...)
        # Клиент автоматически закроется

Доступ к API модулям
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client = YooKassa(api_key="your_key", shop_id=12345)

    # Модули API
    payments = client.payments      # Работа с платежами
    refunds = client.refunds        # Возвраты
    receipts = client.receipts      # Чеки
    invoices = client.invoices      # Счета
    payment_methods = client.payment_methods  # Способы оплаты

