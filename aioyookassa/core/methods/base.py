from typing import Any, Generic, Literal, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

# HTTP method types for better type checking
HTTPMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


class APIMethod(Generic[T]):
    """
    Base API method.
    """

    http_method: HTTPMethod = "GET"
    path: str

    @staticmethod
    def _safe_model_dump(
        obj: Any, exclude_none: bool = False, mode: str = "python"
    ) -> Any:
        """
        Safely dump Pydantic model to dict, return as-is if already dict.

        :param obj: Object to dump (Pydantic model, dict, or other)
        :param exclude_none: Whether to exclude None values
        :param mode: Serialization mode
        :return: Dictionary representation or original object
        """
        if obj is None:
            return None
        if isinstance(obj, BaseModel):
            return obj.model_dump(exclude_none=exclude_none, mode=mode)
        if isinstance(obj, dict):
            return obj
        return obj


class BaseAPIMethod(APIMethod):
    """
    Base class for API methods with common initialization and build logic.
    """

    def __init__(self, path: Optional[str] = None) -> None:
        """
        Initialize API method.

        :param path: Optional custom path to override default.
        """
        if path:
            self.path = path

    @classmethod
    def build(cls, **kwargs: str) -> "BaseAPIMethod":
        """
        Build method for resource-specific endpoints.

        :param kwargs: Resource ID parameters (e.g., payment_id, refund_id, etc.).
        :return: Method instance with formatted path.
        :raises ValueError: If path formatting fails due to missing or invalid parameters.
        """
        if not kwargs:
            return cls()
        try:
            # Format path with the provided ID parameters
            path = cls.path.format(**kwargs)
        except KeyError as e:
            missing_key = str(e).strip("'\"")
            raise ValueError(
                f"Missing required parameter '{missing_key}' for path '{cls.path}'. "
                f"Provided parameters: {list(kwargs.keys())}"
            ) from e
        except Exception as e:
            raise ValueError(
                f"Failed to format path '{cls.path}' with parameters {kwargs}: {str(e)}"
            ) from e
        return cls(path=path)
