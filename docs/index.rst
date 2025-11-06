..

aioyookassa Documentation
=========================

**Асинхронная Python библиотека для работы с API YooKassa**

`aioyookassa` — это современная асинхронная библиотека для интеграции с платежным сервисом YooKassa. Библиотека предоставляет удобный интерфейс для работы с платежами, возвратами, чеками и другими функциями YooKassa API.

.. image:: https://pepy.tech/badge/aioyookassa
   :target: https://pepy.tech/project/aioyookassa
   :alt: Downloads

.. image:: https://pepy.tech/badge/aioyookassa/month
   :target: https://pepy.tech/project/aioyookassa
   :alt: Downloads per month

.. image:: https://api.codiga.io/project/34833/score/svg
   :target: https://api.codiga.io/project/34833/score/svg
   :alt: Code Quality Score

.. image:: https://api.codiga.io/project/34833/status/svg
   :target: https://api.codiga.io/project/34833/status/svg
   :alt: Code Grade

✨ **Особенности**
------------------

* 🚀 **Асинхронность** — полная поддержка `asyncio` для высокопроизводительных приложений
* 🛡️ **Типизация** — полная поддержка типов с использованием Pydantic моделей
* 🔧 **Простота** — интуитивно понятный API для быстрой интеграции
* 📚 **Документация** — подробная документация с примерами использования
* 🧪 **Тестирование** — 90% покрытие кода тестами
* ⚡ **Производительность** — оптимизированная работа с HTTP запросами

🚀 **Быстрый старт**
-------------------

.. code-block:: python

    import asyncio
    from datetime import datetime
    from aioyookassa import YooKassa
    from aioyookassa.types.payment import PaymentAmount, Confirmation
    from aioyookassa.types.enum import PaymentStatus, ConfirmationType, Currency

    async def main():
        # Инициализация клиента
        client = YooKassa(api_key="your_api_key", shop_id=12345)
        
        # Создание платежа
        payment = await client.payments.create_payment(
            amount=PaymentAmount(value=100.00, currency=Currency.RUB),
            confirmation=Confirmation(type=ConfirmationType.REDIRECT, return_url="https://example.com/return"),
            description="Тестовый платеж"
        )
        
        print(f"Payment created: {payment.id}")
        print(f"Confirmation URL: {payment.confirmation.url}")
        
        # Закрытие клиента
        await client.close()

    # Запуск
    asyncio.run(main())

📖 **Содержание**
----------------

.. toctree::
   :maxdepth: 2
   
   installation
   getting-started/index
   api-reference/index
   types/index
   examples/index
   changelog
   contributing

🔗 **Ссылки**
-------------

* `GitHub Repository <https://github.com/your-repo/aioyookassa>`_
* `PyPI Package <https://pypi.org/project/aioyookassa/>`_
* `YooKassa API Documentation <https://yookassa.ru/developers/api>`_

💝 **Поддержка проекта**
-----------------------

Если библиотека оказалась полезной, вы можете поддержать проект:

* `Tribute <https://t.me/tribute/app?startapp=dzqR>`_ — поддержка через Telegram
* `Telegram разработчика <https://t.me/masaasibaata>`_ — связаться с разработчиком

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
