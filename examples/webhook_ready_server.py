"""
Пример использования готового WebhookServer из contrib.

Этот пример показывает, как быстро запустить готовый сервер
для обработки webhook-уведомлений от YooKassa.
"""

import logging

from aioyookassa.contrib.webhook_server import WebhookServer
from aioyookassa.core.webhook_handler import WebhookHandler
from aioyookassa.types.enum import WebhookEvent
from aioyookassa.types.payment import Payment
from aioyookassa.types.refund import Refund
from aioyookassa.types.payout import Payout

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция для запуска webhook сервера."""
    # Создаем обработчик
    handler = WebhookHandler()

    # Регистрируем callback для успешных платежей
    @handler.register_callback(WebhookEvent.PAYMENT_SUCCEEDED)
    async def on_payment_succeeded(payment: Payment):
        """Обработка успешного платежа."""
        logger.info(f"✅ Платеж {payment.id} успешно выполнен")
        logger.info(f"💰 Сумма: {payment.amount.value} {payment.amount.currency}")
        # Здесь ваша бизнес-логика:
        # - Обновление статуса заказа в БД
        # - Отправка уведомления пользователю
        # - Начисление бонусов и т.д.

    # Регистрируем callback для отмененных платежей
    @handler.register_callback(WebhookEvent.PAYMENT_CANCELED)
    async def on_payment_canceled(payment: Payment):
        """Обработка отмененного платежа."""
        logger.info(f"❌ Платеж {payment.id} отменен")
        # Ваша бизнес-логика:
        # - Освобождение товара
        # - Уведомление пользователя

    # Регистрируем callback для возвратов
    @handler.register_callback(WebhookEvent.REFUND_SUCCEEDED)
    async def on_refund_succeeded(refund: Refund):
        """Обработка успешного возврата."""
        logger.info(f"↩️ Возврат {refund.id} выполнен")
        logger.info(f"💰 Сумма возврата: {refund.amount.value} {refund.amount.currency}")
        # Ваша бизнес-логика:
        # - Обновление статуса заказа
        # - Возврат товара на склад

    # Регистрируем callback для нескольких событий сразу
    @handler.register_callback([
        WebhookEvent.PAYOUT_SUCCEEDED,
        WebhookEvent.PAYOUT_CANCELED,
    ])
    async def on_payout_status_change(payout: Payout):
        """Обработка изменений статуса выплаты."""
        logger.info(f"💸 Выплата {payout.id}: статус {payout.status}")
        # Ваша бизнес-логика

    # Регистрируем callback с паттерном (все события payment.*)
    @handler.register_callback("payment.*")
    async def handle_all_payment_events(payment: Payment):
        """Обработка всех событий платежей."""
        logger.debug(f"Payment event: {payment.id}, status: {payment.status}")

    # Создаем и запускаем сервер
    server = WebhookServer(handler=handler)

    logger.info("🚀 Запуск webhook сервера...")
    logger.info("📡 Сервер будет принимать запросы на http://0.0.0.0:8080/webhook")
    logger.info("⚠️  Убедитесь, что этот URL доступен из интернета для YooKassa")

    # Запускаем сервер (блокирующий вызов)
    server.run(host="0.0.0.0", port=8080, path="/webhook")


if __name__ == "__main__":
    main()

