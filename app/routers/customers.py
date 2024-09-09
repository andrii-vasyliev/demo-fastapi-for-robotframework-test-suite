from pydantic import UUID4
from fastapi import APIRouter, status
from app.postgresql import Cursor
from app.schemas.api import GetCustomerSchema, GetCustomersSchema, CreateCustomerSchema
from app.crud import (
    db_get_customer_by_id,
    db_get_customers_by,
    db_create_customer,
)


router = APIRouter(
    prefix="/api/customers",
    tags=["customers"],
)


@router.post("/", response_model=GetCustomerSchema, status_code=status.HTTP_201_CREATED)
async def create_customer(
    cursor: Cursor, customer_data: CreateCustomerSchema
) -> GetCustomerSchema:
    customer: GetCustomerSchema = await db_create_customer(cursor, customer_data)
    return customer


@router.get(
    "/{customer_id}", response_model=GetCustomerSchema, status_code=status.HTTP_200_OK
)
async def get_customer_by_id(cursor: Cursor, customer_id: UUID4) -> GetCustomerSchema:
    customer: GetCustomerSchema = await db_get_customer_by_id(cursor, customer_id)
    return customer


@router.get("/", response_model=GetCustomersSchema, status_code=status.HTTP_200_OK)
async def get_customers_by(
    cursor: Cursor, name: str | None = None, email: str | None = None
) -> GetCustomersSchema:
    customers: GetCustomersSchema = await db_get_customers_by(cursor, name, email)
    return customers
