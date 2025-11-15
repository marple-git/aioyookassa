"""
Ready-to-use aiohttp web server for YooKassa webhook notifications.
"""

import logging
from typing import Optional

from aiohttp import web

from aioyookassa.core.webhook_handler import WebhookHandler
from aioyookassa.core.webhook_validator import WebhookIPValidator

logger = logging.getLogger(__name__)

DEFAULT_WEBHOOK_PATH = "/webhook"


class WebhookServer:
    """
    Ready-to-use aiohttp server for handling YooKassa webhook notifications.

    Provides a complete HTTP server setup with IP validation and event handling.
    """

    def __init__(
        self,
        handler: Optional[WebhookHandler] = None,
        validator: Optional[WebhookIPValidator] = None,
        validate_ip: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize webhook server.

        :param handler: WebhookHandler instance. If None, creates new one.
        :param validator: IP validator instance. If None, uses default.
        :param validate_ip: Whether to validate IP addresses. Default: True.
        :param logger: Logger instance. If None, uses default logger.
        """
        self.logger = logger if logger is not None else logging.getLogger(__name__)
        if handler is None:
            validator = validator if validator is not None else WebhookIPValidator()
            handler = WebhookHandler(validator=validator, logger=self.logger)
        self.handler = handler
        self.validate_ip = validate_ip
        self.logger.info(f"Initialized WebhookServer: validate_ip={validate_ip}")

    def create_app(self) -> web.Application:
        """
        Create aiohttp application with webhook endpoint.

        :return: Configured aiohttp Application instance.
        """
        app = web.Application()
        app.router.add_post(DEFAULT_WEBHOOK_PATH, self._handle_webhook)
        return app

    async def _handle_webhook(self, request: web.Request) -> web.Response:
        """
        Handle incoming webhook request.

        :param request: aiohttp Request object.
        :return: HTTP 200 response on success.
        """
        # Get client IP
        client_ip = request.remote
        self.logger.info(f"Received webhook request from IP: {client_ip}")

        # Validate IP if enabled
        if self.validate_ip:
            if client_ip is None or not self.handler.validator.is_allowed(client_ip):
                self.logger.warning(
                    f"Rejected webhook request from unauthorized IP: {client_ip}"
                )
                raise web.HTTPForbidden(
                    text=f"IP address {client_ip} is not in whitelist"
                )
            self.logger.debug(f"IP validation passed: {client_ip}")

        # Parse request body
        try:
            data = await request.json()
            self.logger.debug(
                f"Parsed request JSON: event={data.get('event', 'unknown')}"
            )
        except Exception as e:
            self.logger.error(f"Failed to parse request JSON: {e}")
            raise web.HTTPBadRequest(text=f"Invalid JSON: {str(e)}") from e

        # Parse and handle notification
        try:
            notification = self.handler.parse_notification(data)
            event_object = await self.handler.handle_notification(notification)
            self.logger.info(
                f"Successfully processed webhook: event={notification.event}, "
                f"object_type={type(event_object).__name__}"
            )
        except Exception as e:
            self.logger.error(f"Error processing webhook: {e}", exc_info=True)
            raise web.HTTPBadRequest(text=f"Error processing webhook: {str(e)}") from e

        # Return 200 to confirm receipt
        self.logger.debug("Returning HTTP 200 response")
        return web.Response(status=200, text="OK")

    def run(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        path: str = DEFAULT_WEBHOOK_PATH,
    ) -> None:
        """
        Run webhook server.

        :param host: Host to bind to. Default: 0.0.0.0.
        :param port: Port to bind to. Default: 8080.
        :param path: Webhook endpoint path. Default: /webhook.
        """
        app = self.create_app()
        if path != DEFAULT_WEBHOOK_PATH:
            # Update route if custom path provided
            # Create new app with custom path
            app = web.Application()
            app.router.add_post(path, self._handle_webhook)
        self.logger.info(f"Starting webhook server on {host}:{port}{path}")
        web.run_app(app, host=host, port=port)
