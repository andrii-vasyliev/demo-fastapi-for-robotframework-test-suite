"""
This module contains functions to interact with the database.
It includes functions to create a new customer, retrieve a customer by ID, and retrieve customers by name or email.
The functions handle exceptions and raise appropriate exceptions based on the error cases.
"""

from typing import Any
from pydantic import UUID4
from psycopg.errors import AssertFailure, NoDataFound
from app.postgresql import get_cursor
from app.exceptions import (
    CREATE_CUSTOMER_ALREADY_EXIST,
    CREATE_CUSTOMER_NOT_CREATED,
    CREATE_CUSTOMER_NOT_FETCHED,
    GET_CUSTOMER_BAD_REQUEST,
    GET_CUSTOMER_NOT_FETCHED,
    GET_CUSTOMER_NOT_FOUND_404,
    GET_CUSTOMER_NOT_FOUND_500,
)
from app.schemas import (
    CreateCustomerSchema,
    GetCustomerSchema,
    GetCustomersSchema,
)


async def create_customer(customer_data: CreateCustomerSchema) -> GetCustomerSchema:
    try:
        async with get_cursor() as cursor:
            await cursor.execute(
                "select create_customer(%s)",
                [
                    customer_data.model_dump_json(),
                ],
            )
            record: tuple[Any, ...] | None = await cursor.fetchone()
            if not record:
                raise CREATE_CUSTOMER_NOT_FETCHED
            customer: GetCustomerSchema = record[0]

    except Exception as e:
        if isinstance(e, AssertFailure):
            raise CREATE_CUSTOMER_ALREADY_EXIST
        else:
            raise CREATE_CUSTOMER_NOT_CREATED

    return customer


async def get_customer_by_id(customer_id: UUID4) -> GetCustomerSchema:
    try:
        async with get_cursor() as cursor:
            await cursor.execute(
                "select get_customer_by_id(%s)",
                [
                    customer_id,
                ],
            )
            record: tuple[Any, ...] | None = await cursor.fetchone()
            if not record:
                raise GET_CUSTOMER_NOT_FETCHED
            customer: GetCustomerSchema = record[0]

    except Exception as e:
        if isinstance(e, AssertFailure):
            raise GET_CUSTOMER_BAD_REQUEST
        elif isinstance(e, NoDataFound):
            raise GET_CUSTOMER_NOT_FOUND_404
        else:
            raise GET_CUSTOMER_NOT_FOUND_500

    return customer


async def get_customers_by(
    name: str | None,
    email: str | None,
) -> GetCustomersSchema:
    try:
        async with get_cursor() as cursor:
            await cursor.execute(
                "select get_customer_by(%s, %s)",
                [
                    name,
                    email,
                ],
            )
            record: tuple[Any, ...] | None = await cursor.fetchone()
            if not record:
                raise GET_CUSTOMER_NOT_FETCHED
            customers: GetCustomersSchema = record[0]

    except Exception as e:
        if isinstance(e, AssertFailure):
            raise GET_CUSTOMER_BAD_REQUEST
        elif isinstance(e, NoDataFound):
            raise GET_CUSTOMER_NOT_FOUND_404
        else:
            raise GET_CUSTOMER_NOT_FOUND_500

    return customers


__all__ = [
    "create_customer",
    "get_customer_by_id",
    "get_customers_by",
]
