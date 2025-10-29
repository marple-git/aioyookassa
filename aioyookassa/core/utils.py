import uuid


def generate_idempotence_key() -> str:
    """
    Generate a unique idempotence key for requests.

    :returns: UUID string.
    :rtype: str
    :seealso: https://yookassa.ru/developers/api/idempotence/
    """
    return str(uuid.uuid4())
