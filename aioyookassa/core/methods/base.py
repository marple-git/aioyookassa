import abc


class APIMethod(abc.ABC):
    """
    Base API Method
    """
    http_method: str = "GET"
    path: str

    @staticmethod
    def build_params(**kwargs) -> dict:
        """
        Build request Params
        :param kwargs:
        :return:
        """
