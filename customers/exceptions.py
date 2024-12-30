"""
This module defines custom exceptions for the application for different scenarios.
"""

from common.exceptions import AppException
from fastapi import status


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

__all__: list[str] = [
    "CREATE_CUSTOMER_NOT_FETCHED",
    "CREATE_CUSTOMER_NOT_CREATED",
    "CREATE_CUSTOMER_ALREADY_EXIST",
    "GET_CUSTOMER_NOT_FETCHED",
    "GET_CUSTOMER_NOT_FOUND_404",
    "GET_CUSTOMER_NOT_FOUND_500",
    "GET_CUSTOMER_BAD_REQUEST",
]
