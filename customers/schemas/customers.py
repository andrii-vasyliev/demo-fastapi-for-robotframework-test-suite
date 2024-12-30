"""
This module defines the schemas for the /api/customers endpoint.

The CreateCustomerSchema class represents a customer to be created with fields for name and email.
The GetCustomerSchema class represents a customer to be returned with fields for id, name, and email.
The GetCustomersSchema class represents a list of customers to be returned.

Each class includes field validation and documentation examples for each field.
"""

import re
from pydantic import BaseModel, ConfigDict, EmailStr, UUID4, field_validator


class CreateCustomerSchema(BaseModel):
    """
    Create Customer request object
    """

    name: str
    email: EmailStr | None = None

    @field_validator("name")
    @classmethod
    def name_validator(cls, v: str) -> str:
        """
        Validate name field
        """
        # Check if name is not empty and contains only allowed chars
        name: str = v.strip()
        if not name:
            raise ValueError("Field 'name' cannot be empty")
        if not re.sub(r"[ \\/\.'&,_\-+@]", "", name).isalnum():
            raise ValueError("Field 'name' must contain only allowed chars")
        if len(name) > 256:
            raise ValueError("Field 'name' must not be greater than 256 characters")
        return name

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
    Get Customer response object
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
    Get Customers response object
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


__all__: list[str] = [
    "CreateCustomerSchema",
    "GetCustomerSchema",
    "GetCustomersSchema",
]
