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
    payouts = client.payouts        # Выплаты
    self_employed = client.self_employed  # Самозанятые
    sbp_banks = client.sbp_banks    # Участники СБП
    personal_data = client.personal_data  # Персональные данные
    deals = client.deals            # Безопасные сделки
    webhooks = client.webhooks      # Webhooks (требует OAuth токен)

Получение информации о настройках магазина или шлюза
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def get_settings():
        async with YooKassa(api_key="your_api_key", shop_id=12345) as client:
            # Получение настроек магазина
            settings = await client.get_me()
            
            print(f"Account ID: {settings.account_id}")
            print(f"Status: {settings.status}")
            print(f"Test mode: {settings.test}")
            
            if settings.fiscalization:
                print(f"Fiscalization enabled: {settings.fiscalization.enabled}")
                print(f"Provider: {settings.fiscalization.provider}")
            
            if settings.payment_methods:
                print(f"Available payment methods: {settings.payment_methods}")
            
            if settings.itn:
                print(f"ITN: {settings.itn}")
            
            # Для Сплитования платежей - получение настроек магазина продавца
            seller_settings = await client.get_me(on_behalf_of="seller_shop_id")
            print(f"Seller account ID: {seller_settings.account_id}")

    asyncio.run(get_settings())

