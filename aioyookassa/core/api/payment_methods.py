from typing import Any, Dict, Union

from aioyookassa.core.api.base import BaseAPI
from aioyookassa.core.methods import CreatePaymentMethod, GetPaymentMethod
from aioyookassa.types.params import CreatePaymentMethodParams
from aioyookassa.types.payment import PaymentMethod


class PaymentMethodsAPI(BaseAPI[CreatePaymentMethodParams, PaymentMethod]):
    """
    YooKassa payment methods API client.

    Provides methods for creating and retrieving payment methods.
    """

    async def create_payment_method(
        self, params: Union[CreatePaymentMethodParams, dict, None] = None, **kwargs: Any
    ) -> PaymentMethod:
        # Note: Union with dict kept for backward compatibility with kwargs support
        """
        Create a new payment method in YooKassa.

        :param params: Payment method parameters (CreatePaymentMethodParams or dict).
        :type params: Union[CreatePaymentMethodParams, dict, None]
        :param kwargs: Additional parameters (merged with params if params is None or dict).
        :returns: PaymentMethod object.
        :rtype: PaymentMethod
        :seealso: https://yookassa.ru/developers/api#create_payment_method

        Example:
            >>> from aioyookassa.types.params import (
            ...     CreatePaymentMethodParams,
            ...     PaymentMethodCardData,
            ...     PaymentMethodHolder,
            ...     PaymentMethodConfirmation
            ... )
            >>> params = CreatePaymentMethodParams(
            ...     type="bank_card",
            ...     card=PaymentMethodCardData(
            ...         number="5555555555554444",
            ...         expiry_year="2025",
            ...         expiry_month="12",
            ...         cardholder="John Doe",
            ...         csc="123"
            ...     ),
            ...     holder=PaymentMethodHolder(gateway_id="gateway_123"),
            ...     confirmation=PaymentMethodConfirmation(
            ...         type="redirect",
            ...         return_url="https://example.com/return"
            ...     )
            ... )
            >>> payment_method = await client.payment_methods.create_payment_method(params)
        """
        # If params is None, use kwargs
        if params is None:
            params = kwargs
        elif isinstance(params, dict):
            params = {**params, **kwargs}

        return await self._create_resource(
            params=params,
            params_class=CreatePaymentMethodParams,
            method_class=CreatePaymentMethod,
            result_class=PaymentMethod,
        )

    async def get_payment_method(self, payment_method_id: str) -> PaymentMethod:
        """
        Retrieve payment method information by ID.

        :param payment_method_id: Payment method identifier.
        :type payment_method_id: str
        :returns: PaymentMethod object.
        :rtype: PaymentMethod
        :seealso: https://yookassa.ru/developers/api#get_payment_method
        """
        return await self._get_by_id(
            resource_id=payment_method_id,
            method_class=GetPaymentMethod,
            result_class=PaymentMethod,
            id_param_name="payment_method_id",
        )
