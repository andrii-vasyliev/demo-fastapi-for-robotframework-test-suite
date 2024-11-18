"""
This module defines the schemas for the /api/orders endpoint.

The CreateOrderItemSchema class represents an order item to be created with fields for item_id and quantity.
The GetOrderItemSchema class represents an order item to be returned with fields for id, item_id, name, price, and quantity.

The CreateOrderSchema class represents an order to be created with fields for customer_id and items.
The GetOrderSchema class represents an order to be returned with fields for id, customer_id, items, and created_at.
The GetCustomerOrdersSchema class represents a list of customer's orders to be returned.

Each class includes field validation and documentation examples for each field.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, UUID4, field_validator


class CreateOrderItemSchema(BaseModel):
    """
    Create Order Item request object
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
    Get Order Item response object
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
    Create Order request object
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
    Get Order response object
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


class GetCustomerOrdersSchema(BaseModel):
    """
    Get Customer Orders response object
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


__all__ = [
    "CreateOrderItemSchema",
    "GetOrderItemSchema",
    "CreateOrderSchema",
    "GetOrderSchema",
    "GetCustomerOrdersSchema",
]
