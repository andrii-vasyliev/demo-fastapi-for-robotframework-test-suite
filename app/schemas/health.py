"""
This module defines the schemas for the /health endpoint.

It includes the HealthStatus enum (UP, PG_DOWN), and the HealthSchema class.

The HealthSchema class represent the health status of the application.
The HealthStatus enum is used to represent the health status of the application, and the timestamp field is used
to store the time when the health check was performed.
"""

from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel


class HealthStatus(StrEnum):
    UP = "UP"
    PG_DOWN = "PG_DOWN"


class HealthSchema(BaseModel):
    """
    Health check object.

    Attributes:
        status (HealthStatus): The health status of the application.
        timestamp (datetime | None): The time when the health check was performed.
    """

    status: HealthStatus
    timestamp: datetime | None


__all__ = [
    "HealthSchema",
    "HealthStatus",
]
