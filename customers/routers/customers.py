"""
This module contains the routes for the customers resource.
It includes routes for creating a new customer, retrieving a customer by id,
and retrieving customers by name and/or email.
The routes return the appropriate response data using schemas for the request data and response data.
"""

from pydantic import UUID4
from fastapi import APIRouter, Request, status
from api.validations import require_json_accept
from customers.schemas import (
    GetCustomerSchema,
    GetCustomersSchema,
    CreateCustomerSchema,
)
from customers.crud import (
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
    request: Request, customer_data: CreateCustomerSchema
) -> GetCustomerSchema:
    """
    Create a new customer.

    Args:
        request (Request): The incoming request object.
        customer_data (CreateCustomerSchema): The customer data to create.

    Returns:
        GetCustomerSchema: The created customer data.
    """
    customer: GetCustomerSchema = await db_create_customer(customer_data)
    return customer


@router.get(
    "/{customer_id}",
    response_model=GetCustomerSchema,
    status_code=status.HTTP_200_OK,
)
@require_json_accept
async def get_customer_by_id(request: Request, customer_id: UUID4) -> GetCustomerSchema:
    """
    Get a customer by their ID.

    Args:
        request (Request): The incoming request object.
        customer_id (UUID4): The ID of the customer to retrieve.

    Returns:
        GetCustomerSchema: The customer data.
    """
    customer: GetCustomerSchema = await db_get_customer_by_id(customer_id)
    return customer


@router.get(
    "/",
    response_model=GetCustomersSchema,
    status_code=status.HTTP_200_OK,
)
@require_json_accept
async def get_customers_by(
    request: Request, name: str | None = None, email: str | None = None
) -> GetCustomersSchema:
    """
    Get customers by name and/or email.

    Args:
        request (Request): The incoming request object.
        name (str | None, optional): The name of the customer to retrieve. Defaults to None.
        email (str | None, optional): The email of the customer to retrieve. Defaults to None.

    Returns:
        GetCustomersSchema: The customer data.
    """
    customers: GetCustomersSchema = await db_get_customers_by(name, email)
    return customers


__all__: list[str] = [
    "router",
]
