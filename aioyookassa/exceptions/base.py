from typing import Any, List, Optional, Type, cast


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
    def _build_detailed_message(
        cls, description: str, message: str, error_details: Optional[dict] = None
    ) -> str:
        """
        Build detailed error message from error details.

        :param description: error code/description
        :param message: error message
        :param error_details: full error response from API
        :return: Detailed error message
        """
        if not error_details:
            return message or description

        parts = [message or description]
        if "parameter" in error_details:
            parts.append(f"Parameter: {error_details['parameter']}")
        if "type" in error_details:
            parts.append(f"Type: {error_details['type']}")
        if "retry_after" in error_details:
            parts.append(f"Retry after: {error_details['retry_after']}")
        return " | ".join(parts)

    @classmethod
    def _find_matching_exception(
        cls, description_lower: str, detailed_message: str
    ) -> Optional[Type["_MatchErrorMixin"]]:
        """
        Find matching exception subclass for the given description.

        :param description_lower: Lowercase error description
        :param detailed_message: Detailed error message
        :return: Matching exception class or None
        """
        for err in cls.__subclasses:
            if err is cls:
                continue
            if err.check(description_lower) and issubclass(err, Exception):
                return err
        return None

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
        detailed_message = cls._build_detailed_message(
            description, message, error_details
        )

        description_lower = description.lower()
        matching_exception = cls._find_matching_exception(
            description_lower, detailed_message
        )

        if matching_exception:
            exception_text = (
                getattr(matching_exception, "text", None) or detailed_message
            )
            exception_cls = cast(Type[Exception], matching_exception)
            raise exception_cls(exception_text)

        # For unknown errors, use description if no error_details (backward compatibility)
        if issubclass(cls, Exception):
            exception_cls = cast(Type[Exception], cls)
            raise exception_cls(detailed_message if error_details else description)


class APIError(Exception, _MatchErrorMixin):
    """
    API Error
    """
