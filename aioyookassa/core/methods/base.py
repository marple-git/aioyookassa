from typing import TypeVar, Generic

T = TypeVar('T')


class APIMethod(Generic[T]):
    """
    Base API Method
    """
    http_method: str = "GET"
    path: str
