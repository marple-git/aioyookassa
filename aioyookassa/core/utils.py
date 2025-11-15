import datetime
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T")


def generate_idempotence_key() -> str:
    """
    Generate a unique idempotence key for requests.

    :returns: UUID string.
    :rtype: str
    :seealso: https://yookassa.ru/developers/api/idempotence/
    """
    return str(uuid.uuid4())


def create_idempotence_headers() -> Dict[str, str]:
    """
    Create headers with idempotence key for requests.

    :returns: Headers dictionary with Idempotence-Key.
    :rtype: Dict[str, str]
    """
    return {"Idempotence-Key": generate_idempotence_key()}


def normalize_params(
    params: Union[BaseModel, dict, None], params_class: Optional[Type[BaseModel]] = None
) -> dict:
    """
    Normalize params to dictionary.

    :param params: Parameters as Pydantic model, dict, or None.
    :param params_class: Optional Pydantic model class for validation.
    :returns: Dictionary of parameters.
    """
    if params is None:
        return {}
    if isinstance(params, dict):
        if params_class:
            return params_class.model_validate(params).model_dump(exclude_none=True)
        return params
    # params is BaseModel at this point due to type annotation
    return params.model_dump(exclude_none=True)


def format_datetime_to_iso(dt: Any) -> Optional[str]:
    """
    Format datetime object to ISO string.

    :param dt: Datetime object or None.
    :returns: ISO formatted string or None.
    """
    if dt is None:
        return None
    if isinstance(dt, datetime.datetime):
        return dt.isoformat()
    if isinstance(dt, str):
        return dt
    return str(dt)


def format_datetime_params(
    params: Dict[str, Any], datetime_fields: List[str]
) -> Dict[str, Any]:
    """
    Format datetime fields in params dictionary to ISO strings.

    :param params: Parameters dictionary.
    :param datetime_fields: List of field names to format.
    :returns: Dictionary with formatted datetime fields.
    """
    formatted = params.copy()
    for field in datetime_fields:
        if field in formatted:
            formatted[field] = format_datetime_to_iso(formatted[field])
    return formatted


def remove_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove None values from dictionary.

    This utility function removes all keys with None values from a dictionary,
    which is commonly needed when building API request parameters.

    :param data: Dictionary to clean.
    :returns: Dictionary without None values.
    :example:
        >>> remove_none_values({"a": 1, "b": None, "c": "value"})
        {"a": 1, "c": "value"}
    """
    return {k: v for k, v in data.items() if v is not None}
