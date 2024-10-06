"""
This module contains the routes for the customers resource.
It includes routes for creating a new customer, retrieving a customer by id,
and retrieving customers by name and/or email.
The routes return the appropriate response data using schemas for the request data and response data.
"""

from pydantic import UUID4
from fastapi import APIRouter, Request, status
from app.postgresql import Cursor
from app.validations import require_json_accept
from app.schemas import GetCustomerSchema, GetCustomersSchema, CreateCustomerSchema
from app.crud import (
    db_get_customer_by_id,
    db_get_customers_by,
    db_create_customer,
)


router = APIRouter(
    prefix="/api/customers",
    tags=["customers"],
)


@router.post(
    "/",
    response_model=GetCustomerSchema,
    status_code=status.HTTP_201_CREATED,
)
@require_json_accept
async def create_customer(
    cursor: Cursor, request: Request, customer_data: CreateCustomerSchema
) -> GetCustomerSchema:
    """
    Create a new customer
    """
    customer: GetCustomerSchema = await db_create_customer(cursor, customer_data)
    return customer


@router.get(
    "/{customer_id}",
    response_model=GetCustomerSchema,
    status_code=status.HTTP_200_OK,
)
@require_json_accept
async def get_customer_by_id(
    cursor: Cursor, request: Request, customer_id: UUID4
) -> GetCustomerSchema:
    """
    Get a customer by id
    """
    customer: GetCustomerSchema = await db_get_customer_by_id(cursor, customer_id)
    return customer


@router.get(
    "/",
    response_model=GetCustomersSchema,
    status_code=status.HTTP_200_OK,
)
@require_json_accept
async def get_customers_by(
    cursor: Cursor, request: Request, name: str | None = None, email: str | None = None
) -> GetCustomersSchema:
    """
    Get customers by name and/or email
    """
    customers: GetCustomersSchema = await db_get_customers_by(cursor, name, email)
    return customers


__all__ = [
    "router",
]
