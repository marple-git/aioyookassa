"""
Пример использования WebhookHandler с независимым веб-фреймворком.

Этот пример показывает, как использовать WebhookHandler
с любым веб-фреймворком (aiohttp, FastAPI, Flask и т.д.).
"""

import asyncio
import logging

from aiohttp import web

from aioyookassa.core.webhook_handler import WebhookHandler
from aioyookassa.core.webhook_validator import WebhookIPValidator
from aioyookassa.exceptions.webhooks import InvalidWebhookIPError
from aioyookassa.types.enum import WebhookEvent
from aioyookassa.types.payment import Payment
from aioyookassa.types.refund import Refund

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Создаем обработчик
handler = WebhookHandler()

# Регистрируем callbacks
@handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
async def on_payment_succeeded(payment: Payment):
    """Обработка успешного платежа."""
    logger.info(f"✅ Платеж {payment.id} успешно выполнен")
    logger.info(f"💰 Сумма: {payment.amount.value} {payment.amount.currency}")
    # Ваша бизнес-логика
    await process_payment(payment)


@handler.register_callback(WebhookEvent.REFUND_SUCCEEDED)
async def on_refund_succeeded(refund: Refund):
    """Обработка успешного возврата."""
    logger.info(f"↩️ Возврат {refund.id} выполнен")
    # Ваша бизнес-логика
    await process_refund(refund)


# Пример бизнес-логики
async def process_payment(payment: Payment):
    """Обработка платежа (пример)."""
    # Здесь ваша логика:
    # - Обновление БД
    # - Отправка уведомлений
    # - Начисление бонусов
    logger.info(f"Обработка платежа {payment.id}...")


async def process_refund(refund: Refund):
    """Обработка возврата (пример)."""
    # Здесь ваша логика:
    # - Обновление статуса заказа
    # - Возврат товара на склад
    logger.info(f"Обработка возврата {refund.id}...")


# ============================================
# Пример 1: Использование с aiohttp
# ============================================

async def aiohttp_webhook_handler(request: web.Request) -> web.Response:
    """
    Обработчик webhook для aiohttp.

    Этот обработчик можно использовать в любом aiohttp приложении.
    """
    # Получаем IP клиента
    client_ip = request.remote

    # Валидация IP (опционально, но рекомендуется)
    if not handler.validator.is_allowed(client_ip):
        logger.warning(f"Rejected request from unauthorized IP: {client_ip}")
        raise web.HTTPForbidden(text=f"IP {client_ip} is not in whitelist")

    # Парсим JSON из запроса
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        raise web.HTTPBadRequest(text=f"Invalid JSON: {str(e)}")

    # Парсим и обрабатываем уведомление
    try:
        notification = handler.parse_notification(data)
        event_object = await handler.handle_notification(notification)
        logger.info(
            f"Successfully processed webhook: event={notification.event}, "
            f"object_type={type(event_object).__name__}"
        )
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise web.HTTPBadRequest(text=f"Error processing webhook: {str(e)}")

    # Возвращаем 200 для подтверждения получения
    return web.Response(status=200, text="OK")


def create_aiohttp_app() -> web.Application:
    """Создает aiohttp приложение с webhook endpoint."""
    app = web.Application()
    app.router.add_post("/webhook", aiohttp_webhook_handler)
    return app


# ============================================
# Пример 2: Использование с FastAPI
# ============================================

try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import Response

    fastapi_app = FastAPI()

    @fastapi_app.post("/webhook")
    async def fastapi_webhook_handler(request: Request):
        """
        Обработчик webhook для FastAPI.

        Этот обработчик можно использовать в любом FastAPI приложении.
        """
        # Получаем IP клиента
        client_ip = request.client.host if request.client else "unknown"

        # Валидация IP
        if not handler.validator.is_allowed(client_ip):
            logger.warning(f"Rejected request from unauthorized IP: {client_ip}")
            raise HTTPException(status_code=403, detail=f"IP {client_ip} is not in whitelist")

        # Парсим JSON
        try:
            data = await request.json()
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")

        # Парсим и обрабатываем уведомление
        try:
            notification = handler.parse_notification(data)
            event_object = await handler.handle_notification(notification)
            logger.info(
                f"Successfully processed webhook: event={notification.event}, "
                f"object_type={type(event_object).__name__}"
            )
        except Exception as e:
            logger.error(f"Error processing webhook: {e}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Error processing webhook: {str(e)}")

        # Возвращаем 200
        return Response(status_code=200, content="OK")

except ImportError:
    # FastAPI не установлен, пропускаем
    fastapi_app = None
    logger.warning("FastAPI not installed, skipping FastAPI example")


# ============================================
# Пример 3: Использование с кастомным валидатором
# ============================================

def create_handler_with_custom_validator():
    """Создает handler с кастомным валидатором IP."""
    # Для разработки/тестирования можно отключить валидацию
    # или использовать свои IP
    custom_validator = WebhookIPValidator(
        allowed_ips=[
            "127.0.0.1",  # localhost для тестирования
            "192.168.1.0/24",  # локальная сеть
            # + стандартные IP YooKassa уже включены по умолчанию
        ]
    )

    custom_handler = WebhookHandler(validator=custom_validator)
    return custom_handler


# ============================================
# Пример 4: Использование без валидации IP (не рекомендуется для production)
# ============================================

def create_handler_without_ip_validation():
    """Создает handler без валидации IP (только для разработки!)."""
    # Создаем валидатор, который разрешает все IP
    permissive_validator = WebhookIPValidator(allowed_ips=["0.0.0.0/0"])

    handler = WebhookHandler(validator=permissive_validator)
    return handler


# ============================================
# Запуск aiohttp сервера (пример)
# ============================================

def main():
    """Запуск aiohttp сервера с webhook обработчиком."""
    app = create_aiohttp_app()

    logger.info("🚀 Запуск webhook сервера на http://0.0.0.0:8080/webhook")
    logger.info("⚠️  Убедитесь, что этот URL доступен из интернета для YooKassa")

    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()

