"""
Definition of API entities
"""

import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, UUID4, field_validator


class ItemSchema(BaseModel):
    """
    Item entity
    """

    id: UUID4
    name: str
    price: float

    @field_validator("name")
    @classmethod
    def name_validator(cls, v: str) -> str:
        if not re.sub(r"[ \\/\.,;\-+()_%@!\'\"]", "", v.strip()).isalnum():
            raise ValueError(
                "Field 'name' cannot be empty and must contain only allowed chars"
            )
        return v.strip()

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "name": "Foo",
                    "price": 42.0,
                }
            ]
        },
    }


class CreateOrderItemSchema(BaseModel):
    """
    Create Order Item request entity
    """

    item_id: UUID4
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_validator(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Field 'quantity' must be greater than 0")
        return v

    model_config: ConfigDict = {
        "extra": "forbid",
        "json_schema_extra": {
            "examples": [
                {
                    "item_id": "00000000-0000-0000-0000-000000000000",
                    "quantity": 42,
                }
            ]
        },
    }


class GetOrderItemSchema(CreateOrderItemSchema):
    """
    Get Order Item response entity
    """

    id: UUID4
    name: str
    price: float

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "item_id": "00000000-0000-0000-0000-000000000000",
                    "name": "Foo",
                    "price": 42.0,
                    "quantity": 42,
                }
            ]
        },
    }


class CreateOrderSchema(BaseModel):
    """
    Create Order request entity
    """

    customer_id: UUID4
    items: list[CreateOrderItemSchema]

    @field_validator("items")
    @classmethod
    def order_items_validator(
        cls, v: list[CreateOrderItemSchema]
    ) -> list[CreateOrderItemSchema]:
        if len(v) == 0:
            raise ValueError("Order cannot be empty")
        return v

    model_config: ConfigDict = {
        "extra": "forbid",
        "json_schema_extra": {
            "examples": [
                {
                    "customer_id": "00000000-0000-0000-0000-000000000000",
                    "items": [
                        {
                            "item_id": "00000000-0000-0000-0000-000000000000",
                            "quantity": 42,
                        }
                    ],
                }
            ]
        },
    }


class GetOrderSchema(BaseModel):
    """
    Get Order response entity
    """

    id: UUID4
    created_at: datetime
    status: str
    items: list[GetOrderItemSchema]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2022-01-01T00:00:00+0000",
                    "status": "New",
                    "items": [
                        {
                            "id": "00000000-0000-0000-0000-000000000000",
                            "item_id": "00000000-0000-0000-0000-000000000000",
                            "name": "Foo",
                            "price": 42.0,
                            "quantity": 42,
                        }
                    ],
                }
            ]
        },
    }


class CreateCustomerSchema(BaseModel):
    """
    Create Customer request entity
    """

    name: str
    email: EmailStr | None = None

    @field_validator("name")
    @classmethod
    def name_validator(cls, v: str) -> str:
        if not re.sub(r"[ \\/\.'&,_\-+@]", "", v.strip()).isalnum():
            raise ValueError(
                "Field 'name' cannot be empty and must contain only allowed chars"
            )
        return v.strip()

    # fmt: off
    model_config: ConfigDict = {
        "extra": "forbid",
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "email": "john@example.com"
                }
            ]
        }
    }
    # fmt: on


class GetCustomerSchema(CreateCustomerSchema):
    """
    Get Customer response entity
    """

    id: UUID4

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "name": "John Doe",
                    "email": "john@example.com",
                }
            ]
        },
    }


class GetCustomersSchema(BaseModel):
    """
    Get Customers response entity
    """

    customers: list[GetCustomerSchema]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "customers": [
                        {
                            "id": "00000000-0000-0000-0000-000000000000",
                            "name": "John Doe",
                            "email": "john@example.com",
                        }
                    ],
                }
            ]
        },
    }


class GetCustomerOrdersSchema(BaseModel):
    """
    Get Customer Orders response entity
    """

    orders: list[GetOrderSchema]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "orders": [
                        {
                            "id": "00000000-0000-0000-0000-000000000000",
                            "created_at": "2022-01-01T00:00:00+0000",
                            "status": "New",
                            "items": [
                                {
                                    "id": "00000000-0000-0000-0000-000000000000",
                                    "item_id": "00000000-0000-0000-0000-000000000000",
                                    "name": "Foo",
                                    "price": 42.0,
                                    "quantity": 42,
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    }
