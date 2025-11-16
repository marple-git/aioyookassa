from datetime import date, datetime
from typing import Any, Dict

from aioyookassa.core.utils import remove_none_values

from .base import APIMethod, BaseAPIMethod


class PersonalDataAPIMethod(BaseAPIMethod):
    """
    Base class for personal data API methods.
    """

    http_method = "GET"
    path = "/personal_data"

    @classmethod
    def build(cls, personal_data_id: str) -> "PersonalDataAPIMethod":  # type: ignore[override]
        """
        Build method for personal data-specific endpoints.

        :param personal_data_id: Personal data ID
        :return: Method instance
        """
        result = super().build(personal_data_id=personal_data_id)
        return result  # type: ignore[return-value]


class CreatePersonalData(PersonalDataAPIMethod):
    """
    Create personal data.
    """

    http_method = "POST"  # type: ignore[assignment]

    @staticmethod
    def build_params(**kwargs: Any) -> Dict[str, Any]:
        # Handle birthdate - convert datetime/date to ISO 8601 string if needed
        birthdate = kwargs.get("birthdate")
        if birthdate is not None and isinstance(birthdate, (datetime, date)):
            kwargs["birthdate"] = birthdate.isoformat()
            # If it's already a string, keep it as is

        params = {
            "type": kwargs.get("type"),
            "last_name": kwargs.get("last_name"),
            "first_name": kwargs.get("first_name"),
            "middle_name": kwargs.get("middle_name"),
            "birthdate": kwargs.get("birthdate"),
            "metadata": kwargs.get("metadata"),
        }
        return remove_none_values(params)


class GetPersonalData(PersonalDataAPIMethod):
    """
    Get personal data.
    """

    http_method = "GET"
    path = "/personal_data/{personal_data_id}"
