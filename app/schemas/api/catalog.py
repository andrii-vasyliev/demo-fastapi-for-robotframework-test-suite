"""
This module defines the schemas for the /api/catalog endpoint.

The ItemSchema class represents an item in the catalog with fields for id, name, and price.
The schema includes field validation and documentation examples for each field.
"""

import re
from pydantic import BaseModel, ConfigDict, UUID4, field_validator


class ItemSchema(BaseModel):
    """
    Item object
    """

    id: UUID4
    name: str
    price: float

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
        if not re.sub(r"[ \\/\.,;\-+()_%@!\'\"]", "", name).isalnum():
            raise ValueError("Field 'name' must contain only allowed chars")
        if len(name) > 512:
            raise ValueError("Field 'name' must not be greater than 512 characters")
        return name

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


__all__ = [
    "ItemSchema",
]
