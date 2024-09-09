"""
Custom Application exception
"""

from typing import Any
from fastapi import status


class AppException(Exception):
    def __init__(
        self, status_code: int, location: list[str | int], message: str, exc_type: str
    ):
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
