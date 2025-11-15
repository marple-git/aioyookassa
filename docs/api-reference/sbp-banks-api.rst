SBP Banks API
=============

API для получения списка участников СБП (Система быстрых платежей).

.. autoclass:: aioyookassa.core.api.sbp_banks.SbpBanksAPI
   :members:
   :show-inheritance:

Методы
------

get_sbp_banks
~~~~~~~~~~~~~

Получение списка участников СБП.

.. code-block:: python

    banks = await client.sbp_banks.get_sbp_banks()
    
    if banks.list:
        for bank in banks.list:
            print(f"{bank.name} (BIC: {bank.bic}, ID: {bank.bank_id})")
    
    # Использование идентификатора банка для создания выплаты
    if banks.list:
        bank_id = banks.list[0].bank_id
        # Используйте bank_id в CreatePayoutParams для выплаты через СБП

