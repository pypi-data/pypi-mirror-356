import os
import uuid


def get_request_id() -> str:
    """Return a correlation id for logging."""
    return os.getenv("REQUEST_ID", str(uuid.uuid4()))
