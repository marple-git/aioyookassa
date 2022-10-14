from typing import TypeVar, Generic

T = TypeVar('T')


class APIMethod(Generic[T]):
    """
    Base API Method
    """
    http_method: str = "GET"
    path: str


class PaymentMethod(APIMethod):
    """
    Payment Method
    """
    http_method = "GET"
    path = "/payments"

    def __init__(self, path: str):
        self.path = path

    @classmethod
    def build(cls, payment_id):
        """
        Build method
        :param payment_id: Payment ID
        :return: Method
        """
        path = cls.path.format(payment_id=payment_id)
        return cls(path=path)
