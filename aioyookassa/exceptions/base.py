from typing import Optional, List


class _MatchErrorMixin:
    """Base class for all exceptions raised by this module."""
    match = ''
    text: Optional[str] = None

    __subclasses: List = []

    def __init_subclass__(cls, **kwargs):
        super(_MatchErrorMixin, cls).__init_subclass__(**kwargs)
        if not hasattr(cls, f"_{cls.__name__}__group"):
            cls.__subclasses.append(cls)

    @classmethod
    def check(cls, message) -> bool:
        """
        Compare pattern with message
        :param message: always must be in lowercase
        :return: bool
        """
        return cls.match.lower() in message

    @classmethod
    def get_text(cls, message) -> str:
        """
        Get text from message
        :param message: always must be in lowercase
        :return: str
        """
        return cls.text or message

    @classmethod
    def detect(cls, description, message):
        """
        Find existing exception
        :param description: error description
        :return:
        """
        description = description.lower()
        for err in cls.__subclasses:
            if err is cls:
                continue
            if err.check(description):
                raise err(err.text or message or description)
        raise cls(description)


class APIError(Exception, _MatchErrorMixin):
    """
    API Error
    """
