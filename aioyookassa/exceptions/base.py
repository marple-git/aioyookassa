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
    def detect(cls, description: str, message: str) -> None:
        """
        Find existing exception
        :param description: error description
        :return:
        """
        description = description.lower()
        for err in cls.__subclasses:
            if err is cls:
                continue
            if err.check(description) and issubclass(err, Exception):
                raise err(err.text or message or description)
        if issubclass(cls, Exception):
            raise cls(description)


class APIError(Exception, _MatchErrorMixin):
    """
    API Error
    """
