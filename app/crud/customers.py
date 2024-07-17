from pydantic import UUID4
from fastapi import status
from psycopg import AsyncCursor
from psycopg.errors import AssertFailure, NoDataFound
from exceptions import AppException
from schemas.api import CreateCustomerSchema, GetCustomerSchema, GetCustomersSchema


CREATE_CUSTOMER_NOT_FETCHED: dict = {
    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "location": [
        "db",
        "create_customer",
    ],
    "message": "Customer not fetched",
    "exc_type": "not_fetched",
}

CREATE_CUSTOMER_NOT_CREATED: dict = {
    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "location": [
        "db",
        "create_customer",
    ],
    "message": "Customer not created",
    "exc_type": "not_created",
}

CREATE_CUSTOMER_ALREADY_EXIST: dict = {
    "status_code": status.HTTP_409_CONFLICT,
    "location": [
        "db",
        "create_customer",
    ],
    "message": "Customer already exist",
    "exc_type": "bad_request",
}

GET_CUSTOMER_NOT_FETCHED: dict = {
    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "location": [
        "db",
        "get_customer",
    ],
    "message": "Customer not fetched",
    "exc_type": "not_fetched",
}

GET_CUSTOMER_NOT_FOUND_404: dict = {
    "status_code": status.HTTP_404_NOT_FOUND,
    "location": [
        "db",
        "get_customer",
    ],
    "message": "Customer not found",
    "exc_type": "not_found",
}

GET_CUSTOMER_NOT_FOUND_500: dict = {
    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "location": [
        "db",
        "get_customer",
    ],
    "message": "Customer not found",
    "exc_type": "not_found",
}

GET_CUSTOMER_BAD_REQUEST: dict = {
    "status_code": status.HTTP_400_BAD_REQUEST,
    "location": [
        "db",
        "get_customer",
    ],
    "message": "At least one search parameter is required",
    "exc_type": "bad_request",
}


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
            raise AppException(**CREATE_CUSTOMER_NOT_FETCHED)

        customer: GetCustomerSchema = record[0]
    except Exception as e:
        if isinstance(e, AssertFailure):
            raise AppException(**CREATE_CUSTOMER_ALREADY_EXIST)
        else:
            raise AppException(**CREATE_CUSTOMER_NOT_CREATED)

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
            raise AppException(**GET_CUSTOMER_NOT_FETCHED)

        customer: GetCustomerSchema = record[0]
    except Exception as e:
        if isinstance(e, NoDataFound):
            raise AppException(**GET_CUSTOMER_NOT_FOUND_404)
        else:
            raise AppException(**GET_CUSTOMER_NOT_FOUND_500)

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
            raise AppException(**GET_CUSTOMER_NOT_FETCHED)

        customers: GetCustomersSchema = record[0]
    except Exception as e:
        if isinstance(e, AssertFailure):
            raise AppException(**GET_CUSTOMER_BAD_REQUEST)
        elif isinstance(e, NoDataFound):
            raise AppException(**GET_CUSTOMER_NOT_FOUND_404)
        else:
            raise AppException(**GET_CUSTOMER_NOT_FOUND_500)

    return customers
