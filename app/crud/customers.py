from pydantic import UUID4
from psycopg import AsyncCursor
from psycopg.errors import AssertFailure, NoDataFound
from app.exceptions import (
    CREATE_CUSTOMER_ALREADY_EXIST,
    CREATE_CUSTOMER_NOT_CREATED,
    CREATE_CUSTOMER_NOT_FETCHED,
    GET_CUSTOMER_BAD_REQUEST,
    GET_CUSTOMER_NOT_FETCHED,
    GET_CUSTOMER_NOT_FOUND_404,
    GET_CUSTOMER_NOT_FOUND_500,
)
from app.schemas.api import CreateCustomerSchema, GetCustomerSchema, GetCustomersSchema


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
            raise CREATE_CUSTOMER_NOT_FETCHED

        customer: GetCustomerSchema = record[0]
    except Exception as e:
        if isinstance(e, AssertFailure):
            raise CREATE_CUSTOMER_ALREADY_EXIST
        else:
            raise CREATE_CUSTOMER_NOT_CREATED

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
            raise GET_CUSTOMER_NOT_FETCHED

        customer: GetCustomerSchema = record[0]
    except Exception as e:
        if isinstance(e, NoDataFound):
            raise GET_CUSTOMER_NOT_FOUND_404
        else:
            raise GET_CUSTOMER_NOT_FOUND_500

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
