"""
Custom Application exception

This module defines custom exceptions for the application.
It provides a base class `AppException` and several predefined exceptions
for different scenarios, such as `MUST_ACCEPT_JSON`, `HTTP_NOT_FOUND`,
`CREATE_CUSTOMER_NOT_FETCHED`, `CREATE_CUSTOMER_NOT_CREATED`,
`CREATE_CUSTOMER_ALREADY_EXIST`, `GET_CUSTOMER_NOT_FETCHED`,
`GET_CUSTOMER_NOT_FOUND_404`, and `GET_CUSTOMER_NOT_FOUND_500`.

Each exception is an instance of the `AppException` class, which takes the following arguments:
- `status_code`: The HTTP status code associated with the exception.
- `location`: A list representing the location of the error in the request.
- `message`: A descriptive message about the error.
- `exc_type`: A string representing the type of exception.

The `content` method returns a dictionary containing the error details in a format suitable for returning as the response body.

These exceptions can be used throughout the application to raise and handle specific error scenarios.
For example, in the `create_customer` function, you could raise `CREATE_CUSTOMER_NOT_FETCHED`
if the customer data could not be fetched from the database. The `get_customer` function
could raise `GET_CUSTOMER_NOT_FOUND_404` if the customer is not found in the database.
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

CREATE_CUSTOMER_NOT_FETCHED: AppException = AppException(
    status.HTTP_500_INTERNAL_SERVER_ERROR,
    [
        "db",
        "create_customer",
    ],
    "Customer not fetched",
    "not_fetched",
)

CREATE_CUSTOMER_NOT_CREATED: AppException = AppException(
    status.HTTP_500_INTERNAL_SERVER_ERROR,
    [
        "db",
        "create_customer",
    ],
    "Customer not created",
    "not_created",
)

CREATE_CUSTOMER_ALREADY_EXIST: AppException = AppException(
    status.HTTP_409_CONFLICT,
    [
        "db",
        "create_customer",
    ],
    "Customer already exist",
    "bad_request",
)

GET_CUSTOMER_NOT_FETCHED: AppException = AppException(
    status.HTTP_500_INTERNAL_SERVER_ERROR,
    [
        "db",
        "get_customer",
    ],
    "Customer not fetched",
    "not_fetched",
)

GET_CUSTOMER_NOT_FOUND_404: AppException = AppException(
    status.HTTP_404_NOT_FOUND,
    [
        "db",
        "get_customer",
    ],
    "Customer not found",
    "not_found",
)

GET_CUSTOMER_NOT_FOUND_500: AppException = AppException(
    status.HTTP_500_INTERNAL_SERVER_ERROR,
    [
        "db",
        "get_customer",
    ],
    "Customer not found",
    "not_found",
)

GET_CUSTOMER_BAD_REQUEST: AppException = AppException(
    status.HTTP_400_BAD_REQUEST,
    [
        "db",
        "get_customer",
    ],
    "At least one search parameter is required",
    "bad_request",
)

__all__ = [
    "AppException",
    "MUST_ACCEPT_JSON",
    "HTTP_NOT_FOUND",
    "CREATE_CUSTOMER_NOT_FETCHED",
    "CREATE_CUSTOMER_NOT_CREATED",
    "CREATE_CUSTOMER_ALREADY_EXIST",
    "GET_CUSTOMER_NOT_FETCHED",
    "GET_CUSTOMER_NOT_FOUND_404",
    "GET_CUSTOMER_NOT_FOUND_500",
    "GET_CUSTOMER_BAD_REQUEST",
]
