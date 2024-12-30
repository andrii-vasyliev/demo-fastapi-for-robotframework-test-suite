"""
This module contains functions to interact with the database.
It includes functions to create a new customer, retrieve a customer by ID, and retrieve customers by name or email.
The functions handle exceptions and raise appropriate exceptions based on the error cases.
"""

from typing import Any
from pydantic import UUID4
from psycopg.errors import AssertFailure, NoDataFound
from common.database.postgresql import get_cursor
from customers.exceptions import (
    CREATE_CUSTOMER_ALREADY_EXIST,
    CREATE_CUSTOMER_NOT_CREATED,
    CREATE_CUSTOMER_NOT_FETCHED,
    GET_CUSTOMER_BAD_REQUEST,
    GET_CUSTOMER_NOT_FETCHED,
    GET_CUSTOMER_NOT_FOUND_404,
    GET_CUSTOMER_NOT_FOUND_500,
)
from customers.schemas import (
    CreateCustomerSchema,
    GetCustomerSchema,
    GetCustomersSchema,
)


async def create_customer(customer_data: CreateCustomerSchema) -> GetCustomerSchema:
    """
    Creates a new customer in the database.

    Args:
        customer_data (CreateCustomerSchema): The customer data to be created.

    Returns:
        GetCustomerSchema: The created customer data.

    Raises:
        CREATE_CUSTOMER_ALREADY_EXIST: If the customer already exists.
        CREATE_CUSTOMER_NOT_CREATED: If the customer could not be created.
        CREATE_CUSTOMER_NOT_FETCHED: If the customer could not be fetched.
    """
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

    except AssertFailure:
        raise CREATE_CUSTOMER_ALREADY_EXIST
    except Exception as e:
        raise CREATE_CUSTOMER_NOT_CREATED

    return customer


async def get_customer_by_id(customer_id: UUID4) -> GetCustomerSchema:
    """
    Retrieves a customer from the database by their ID.

    Args:
        customer_id (UUID4): The ID of the customer to retrieve.

    Returns:
        GetCustomerSchema: The retrieved customer data.

    Raises:
        GET_CUSTOMER_BAD_REQUEST: If the customer ID is invalid.
        GET_CUSTOMER_NOT_FETCHED: If the customer could not be fetched.
        GET_CUSTOMER_NOT_FOUND_404: If the customer was not found.
        GET_CUSTOMER_NOT_FOUND_500: If an error occurred while fetching the customer.
    """
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

    except AssertFailure:
        raise GET_CUSTOMER_BAD_REQUEST
    except NoDataFound:
        raise GET_CUSTOMER_NOT_FOUND_404
    except Exception as e:
        raise GET_CUSTOMER_NOT_FOUND_500

    return customer


async def get_customers_by(
    name: str | None,
    email: str | None,
) -> GetCustomersSchema:
    """
    Retrieves customers from the database by their name or email.

    Args:
        name (str | None): The name of the customer to retrieve.
        email (str | None): The email of the customer to retrieve.

    Returns:
        GetCustomersSchema: The retrieved customers data.

    Raises:
        GET_CUSTOMER_BAD_REQUEST: If the customer name or email is invalid.
        GET_CUSTOMER_NOT_FETCHED: If the customer could not be fetched.
        GET_CUSTOMER_NOT_FOUND_404: If the customer was not found.
        GET_CUSTOMER_NOT_FOUND_500: If an error occurred while fetching the customer.
    """
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

    except AssertFailure:
        raise GET_CUSTOMER_BAD_REQUEST
    except NoDataFound:
        raise GET_CUSTOMER_NOT_FOUND_404
    except Exception as e:
        raise GET_CUSTOMER_NOT_FOUND_500

    return customers


__all__: list[str] = [
    "create_customer",
    "get_customer_by_id",
    "get_customers_by",
]
