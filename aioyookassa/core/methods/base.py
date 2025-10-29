from typing import Generic, TypeVar

T = TypeVar("T")


class APIMethod(Generic[T]):
    """
    Base API method.
    """

    http_method: str = "GET"
    path: str
