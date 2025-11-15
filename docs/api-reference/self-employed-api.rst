Self-Employed API
==================

API для работы с самозанятыми.

.. autoclass:: aioyookassa.core.api.self_employed.SelfEmployedAPI
   :members:
   :show-inheritance:

Методы
------

create_self_employed
~~~~~~~~~~~~~~~~~~~~

Создание нового самозанятого.

.. code-block:: python

    from aioyookassa.types.params import (
        CreateSelfEmployedParams,
        SelfEmployedConfirmationData
    )
    
    params = CreateSelfEmployedParams(
        itn="123456789012",  # ИНН самозанятого (12 цифр)
        confirmation=SelfEmployedConfirmationData(
            type="redirect",
            confirmation_url="https://example.com/confirm"
        )
    )
    self_employed = await client.self_employed.create_self_employed(params)
    
    # Или с телефоном вместо ИНН
    params = CreateSelfEmployedParams(
        phone="79000000000",  # Телефон в формате ITU-T E.164
        confirmation=SelfEmployedConfirmationData(
            type="redirect",
            confirmation_url="https://example.com/confirm"
        )
    )
    self_employed = await client.self_employed.create_self_employed(params)

get_self_employed
~~~~~~~~~~~~~~~~~

Получение информации о самозанятом.

.. code-block:: python

    self_employed = await client.self_employed.get_self_employed("self_employed_id")
    print(f"Status: {self_employed.status}")
    print(f"ITN: {self_employed.itn}")
    print(f"Phone: {self_employed.phone}")

