from pydantic import UUID4
from fastapi import status
from psycopg import AsyncCursor
from psycopg.errors import AssertFailure, NoDataFound
from exceptions import AppException
from schemas.api import CreateCustomerSchema, GetCustomerSchema, GetCustomersSchema


async def create_customer(
    cursor: AsyncCursor, customer_data: CreateCustomerSchema
) -> GetCustomerSchema:
    try:
        await cursor.execute(
            "select create_customer(%s)",
            [
                customer_data.model_dump_json(),
            ],
        )

        record = await cursor.fetchone()
        if not record:
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                [
                    "db",
                    "create_customer",
                ],
                "Customer not fetched",
                "not_fetched",
            )

        customer: GetCustomerSchema = record[0]
    except Exception as e:
        if isinstance(e, AssertFailure):
            raise AppException(
                status.HTTP_409_CONFLICT,
                [
                    "db",
                    "create_customer",
                ],
                "Customer already exist",
                "bad_request",
            )
        else:
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                [
                    "db",
                    "create_customer",
                ],
                "Customer not created",
                "not_created",
            )

    return customer


async def get_customer_by_id(
    cursor: AsyncCursor, customer_id: UUID4
) -> GetCustomerSchema:
    try:
        await cursor.execute(
            "select get_customer_by_id(%s)",
            [
                customer_id,
            ],
        )

        record = await cursor.fetchone()
        if not record:
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                [
                    "db",
                    "get_customer_by_id",
                ],
                "Customer not fetched",
                "not_fetched",
            )

        customer: GetCustomerSchema = record[0]
    except Exception as e:
        if isinstance(e, NoDataFound):
            raise AppException(
                status.HTTP_404_NOT_FOUND,
                [
                    "db",
                    "get_customer_by_id",
                ],
                "Customer not found",
                "no_data_found",
            )
        else:
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                [
                    "db",
                    "get_customer_by_id",
                ],
                "Customer not found",
                "no_data_found",
            )

    return customer


async def get_customers_by(
    cursor: AsyncCursor,
    name: str | None,
    email: str | None,
) -> GetCustomersSchema:
    try:
        await cursor.execute(
            "select get_customer_by(%s, %s)",
            [
                name,
                email,
            ],
        )

        record = await cursor.fetchone()
        if not record:
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                [
                    "db",
                    "get_customer_by",
                ],
                "Customer not fetched",
                "not_fetched",
            )

        customers: GetCustomersSchema = record[0]
    except Exception as e:
        if isinstance(e, AssertFailure):
            raise AppException(
                status.HTTP_400_BAD_REQUEST,
                [
                    "db",
                    "get_customer_by",
                ],
                "At least one search parameter is required",
                "bad_request",
            )
        elif isinstance(e, NoDataFound):
            raise AppException(
                status.HTTP_404_NOT_FOUND,
                [
                    "db",
                    "get_customer_by",
                ],
                "Customer not found",
                "no_data_found",
            )
        else:
            raise AppException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                [
                    "db",
                    "get_customer_by_id",
                ],
                "Customer not found",
                "not_found",
            )

    return customers
