from aioyookassa.core.abc.client import BaseAPIClient
from aioyookassa.core.methods import CreatePaymentMethod, GetPaymentMethod
from aioyookassa.core.utils import generate_idempotence_key
from aioyookassa.types.payment import PaymentMethod


class PaymentMethodsAPI:
    """
    YooKassa payment methods API client.

    Provides methods for creating and retrieving payment methods.
    """

    def __init__(self, client: BaseAPIClient):
        self._client = client

    async def create_payment_method(self, **kwargs) -> PaymentMethod:
        """
        Create a new payment method in YooKassa.

        :param kwargs: Payment method parameters.
        :returns: PaymentMethod object.
        :rtype: PaymentMethod
        :seealso: https://yookassa.ru/developers/api#create_payment_method
        """
        params = CreatePaymentMethod.build_params(**kwargs)
        headers = {"Idempotence-Key": generate_idempotence_key()}
        result = await self._client._send_request(
            CreatePaymentMethod, json=params, headers=headers
        )
        return PaymentMethod(**result)

    async def get_payment_method(self, payment_method_id: str) -> PaymentMethod:
        """
        Retrieve payment method information by ID.

        :param payment_method_id: Payment method identifier.
        :type payment_method_id: str
        :returns: PaymentMethod object.
        :rtype: PaymentMethod
        :seealso: https://yookassa.ru/developers/api#get_payment_method
        """
        method = GetPaymentMethod.build(payment_method_id)
        result = await self._client._send_request(method)
        return PaymentMethod(**result)
