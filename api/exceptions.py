"""
Custom Application exception

Module provides a base class `AppException` and several predefined exceptions
for different scenarios, such as `MUST_ACCEPT_JSON`, `HTTP_NOT_FOUND`, etc.

Each exception is an instance of the `AppException` class, which takes the following arguments:
- `status_code`: The HTTP status code associated with the exception.
- `location`: A list representing the location of the error in the request.
- `message`: A descriptive message about the error.
- `exc_type`: A string representing the type of exception.

The `content` method returns a dictionary containing the error details in a format suitable for returning as the response body.

These exceptions can be used throughout the application to raise and handle specific error scenarios.
"""

from typing import Any
from fastapi import status


class AppException(Exception):
    def __init__(
        self, status_code: int, location: list[str | int], message: str, exc_type: str
    ) -> None:
        self.status_code: int = status_code
        self._location: list[str | int] = location
        self._msg: str = message
        self._exc_type: str = exc_type

    def content(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "detail": [
                {
                    "loc": self._location,
                    "msg": self._msg,
                    "type": self._exc_type,
                }
            ]
        }


MUST_ACCEPT_JSON: AppException = AppException(
    status.HTTP_406_NOT_ACCEPTABLE,
    [
        "http",
        "headers",
        "Accept",
    ],
    "This endpoint only supports application/json responses",
    "not_acceptable",
)


HTTP_NOT_FOUND: AppException = AppException(
    status.HTTP_404_NOT_FOUND,
    [
        "http",
    ],
    "Not found",
    "not_found",
)

__all__: list[str] = [
    "AppException",
    "MUST_ACCEPT_JSON",
    "HTTP_NOT_FOUND",
]
