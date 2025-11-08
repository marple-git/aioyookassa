from typing import Any, List, Optional, Type


class _MatchErrorMixin:
    """Base class for all exceptions raised by this module."""

    match: str = ""
    text: Optional[str] = None

    __subclasses: List[Type["_MatchErrorMixin"]] = []

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super(_MatchErrorMixin, cls).__init_subclass__(**kwargs)
        if not hasattr(cls, f"_{cls.__name__}__group"):
            cls.__subclasses.append(cls)

    @classmethod
    def check(cls, message: str) -> bool:
        """
        Compare pattern with message
        :param message: always must be in lowercase
        :return: bool
        """
        if not cls.match:
            return False
        return cls.match.lower() in message

    @classmethod
    def get_text(cls, message: str) -> str:
        """
        Get text from message
        :param message: always must be in lowercase
        :return: str
        """
        return cls.text or message

    @classmethod
    def detect(
        cls, description: str, message: str, error_details: Optional[dict] = None
    ) -> None:
        """
        Find existing exception
        :param description: error code/description
        :param message: error message
        :param error_details: full error response from API
        :return:
        """
        # Build detailed error message for matched errors
        if error_details:
            parts = [message or description]
            if "parameter" in error_details:
                parts.append(f"Parameter: {error_details['parameter']}")
            if "type" in error_details:
                parts.append(f"Type: {error_details['type']}")
            if "retry_after" in error_details:
                parts.append(f"Retry after: {error_details['retry_after']}")
            detailed_message = " | ".join(parts)
        else:
            detailed_message = message or description

        description_lower = description.lower()
        for err in cls.__subclasses:
            if err is cls:
                continue
            if err.check(description_lower) and issubclass(err, Exception):
                raise err(err.text or detailed_message)

        # For unknown errors, use description if no error_details (backward compatibility)
        if issubclass(cls, Exception):
            raise cls(detailed_message if error_details else description)


class APIError(Exception, _MatchErrorMixin):
    """
    API Error
    """
