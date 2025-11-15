Personal Data API
=================

API для работы с персональными данными получателей выплат.

.. autoclass:: aioyookassa.core.api.personal_data.PersonalDataAPI
   :members:
   :show-inheritance:

Методы
------

create_personal_data
~~~~~~~~~~~~~~~~~~~~

Создание персональных данных.

Для выплат с проверкой получателя (СБП):
.. code-block:: python

    from aioyookassa.types.params import SbpPayoutRecipientData
    from datetime import date
    
    params = SbpPayoutRecipientData(
        type="sbp_payout_recipient",
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович"  # Опционально
    )
    personal_data = await client.personal_data.create_personal_data(params)

Для выплат с передачей данных получателя для выписок из реестра:
.. code-block:: python

    from aioyookassa.types.params import PayoutStatementRecipientData
    from datetime import date
    
    params = PayoutStatementRecipientData(
        type="payout_statement_recipient",
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович",  # Опционально, но обязательно если есть в паспорте
        birthdate=date(1990, 1, 1)  # Дата рождения в формате ISO 8601
    )
    personal_data = await client.personal_data.create_personal_data(params)

get_personal_data
~~~~~~~~~~~~~~~~~

Получение информации о персональных данных.

.. code-block:: python

    personal_data = await client.personal_data.get_personal_data("personal_data_id")
    print(f"Type: {personal_data.type}")
    print(f"Status: {personal_data.status}")
    if personal_data.expires_at:
        print(f"Expires at: {personal_data.expires_at}")

