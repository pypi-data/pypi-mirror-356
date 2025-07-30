from datetime import datetime

from uuid_extension import uuid7


def create_id(
    timestamp: float | datetime | None = None,
    counter: int | None = None,
) -> str:
    """
    Create UUID7 string
    """
    return str(uuid7(timestamp, counter))
