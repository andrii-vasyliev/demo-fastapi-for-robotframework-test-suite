from functools import wraps
from fastapi import Request
from app.exceptions import MUST_ACCEPT_JSON


def require_json_accept(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request | None = kwargs.get("request")
        if request:
            accept_header: str | None = request.headers.get("Accept")
            if not (accept_header and "application/json" in accept_header):
                # If the client doesn't accept JSON, raise an exception
                raise MUST_ACCEPT_JSON

        return await func(*args, **kwargs)

    return wrapper
