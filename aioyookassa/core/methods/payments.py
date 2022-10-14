from aioyookassa.core.methods.base import APIMethod


class CreatePayment(APIMethod):
    """
    Create payment
    """
    http_method = "POST"
    path = "/payments"

    @staticmethod
    def build_params(**kwargs):
        if confirmation := kwargs.get("confirmation"):
            kwargs["confirmation"] = confirmation.dict(exclude_none=True)
        params = {
            "amount": {
                "value": kwargs.get("amount"),
                "currency": kwargs.get("currency")
            },
            "description": kwargs.get("description"),
            "receipt": kwargs.get("receipt"),
            "recipient": kwargs.get("recipient"),
            "payment_token": kwargs.get("payment_token"),
            "payment_method_id": kwargs.get("payment_method_id"),
            "payment_method_data": kwargs.get("payment_method_data"),
            "confirmation": kwargs.get("confirmation"),
            "save_payment_method": kwargs.get("save_payment_method"),
            "capture": kwargs.get("capture"),
            "client_ip": kwargs.get("client_ip"),
            "metadata": kwargs.get("metadata"),
            "airline": kwargs.get("airline"),
            "transfers": kwargs.get("transfers"),
            "deal": kwargs.get("deal"),
            "merchant_customer_id": kwargs.get("merchant_customer_id"),
        }
        return params
