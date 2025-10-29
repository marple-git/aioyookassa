.. highlight:: shell

===============
Installation
===============

.. tip:: Поддерживаемые версии Python: `3.8` и выше

Стабильная версия
------------------

Для установки aioyookassa выполните команду в терминале:

.. code-block:: console

    $ pip install aioyookassa

Установка через Poetry
-----------------------

Если вы используете Poetry для управления зависимостями:

.. code-block:: console

    $ poetry add aioyookassa

Установка из исходного кода
----------------------------

Для установки последней версии из исходного кода:

.. code-block:: console

    $ pip install git+https://github.com/your-repo/aioyookassa.git

Требования
----------

* Python 3.8.1+
* aiohttp
* pydantic

Проверка установки
------------------

После установки вы можете проверить, что библиотека работает корректно:

.. code-block:: python

    import asyncio
    from aioyookassa import YooKassa

    async def test_connection():
        client = YooKassa(api_key="test_key", shop_id=12345)
        print("aioyookassa успешно установлена!")
        await client.close()

    asyncio.run(test_connection())