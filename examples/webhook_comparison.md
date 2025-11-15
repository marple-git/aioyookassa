# Сравнение подходов к обработке webhook-уведомлений

## 1. Готовый сервер (WebhookServer) - для быстрого старта

### Преимущества:

- ✅ Минимум кода - все настроено из коробки
- ✅ Быстрый старт - можно запустить за несколько строк
- ✅ Автоматическая валидация IP
- ✅ Готовая обработка ошибок

### Недостатки:

- ❌ Меньше гибкости в настройке
- ❌ Привязан к aiohttp

### Когда использовать:

- Простые проекты
- Быстрое прототипирование
- Отдельный микросервис для webhook

### Пример:

```python
from aioyookassa.contrib.webhook_server import WebhookServer
from aioyookassa.core.webhook_handler import WebhookHandler
from aioyookassa.types.enum import WebhookEvent

handler = WebhookHandler()

@handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
async def on_payment(payment):
    print(f"Payment {payment.id} succeeded")

server = WebhookServer(handler=handler)
server.run(host="0.0.0.0", port=8080)
```

---

## 2. Независимый обработчик (WebhookHandler) - для гибкости

### Преимущества:

- ✅ Работает с любым веб-фреймворком (aiohttp, FastAPI, Flask, Django)
- ✅ Полный контроль над обработкой запросов
- ✅ Легко интегрировать в существующее приложение
- ✅ Можно настроить middleware, роутинг, логирование

### Недостатки:

- ❌ Нужно больше кода для настройки
- ❌ Нужно самому обрабатывать ошибки

### Когда использовать:

- Интеграция в существующее приложение
- Использование другого фреймворка
- Нужна кастомная логика обработки

### Пример с aiohttp:

```python
from aiohttp import web
from aioyookassa.core.webhook_handler import WebhookHandler

handler = WebhookHandler()

async def webhook_endpoint(request):
    # Валидация IP
    if not handler.validator.is_allowed(request.remote):
        raise web.HTTPForbidden()

    # Обработка
    data = await request.json()
    notification = handler.parse_notification(data)
    await handler.handle_notification(notification)

    return web.Response(status=200)

app = web.Application()
app.router.add_post("/webhook", webhook_endpoint)
web.run_app(app)
```

### Пример с FastAPI:

```python
from fastapi import FastAPI, Request, HTTPException
from aioyookassa.core.webhook_handler import WebhookHandler

handler = WebhookHandler()
app = FastAPI()

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    # Валидация IP
    if not handler.validator.is_allowed(request.client.host):
        raise HTTPException(403)

    # Обработка
    data = await request.json()
    notification = handler.parse_notification(data)
    await handler.handle_notification(notification)

    return {"status": "ok"}
```

---

## Рекомендации

### Для новых проектов:

- Начните с **WebhookServer** для быстрого старта
- Перейдите на **WebhookHandler** если нужна большая гибкость

### Для существующих проектов:

- Используйте **WebhookHandler** для интеграции
- Настройте под свой фреймворк и требования

### Для production:

- Всегда включайте валидацию IP
- Настройте логирование
- Обрабатывайте ошибки
- Используйте HTTPS
- Настройте мониторинг
