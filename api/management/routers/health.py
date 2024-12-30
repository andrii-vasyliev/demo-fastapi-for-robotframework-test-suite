"""
This module contains the health check endpoint for the application.
It provides a simple endpoint to check if the application is running and
the database connection is working correctly.
The endpoint returns a JSON response with the status of the application
and the current timestamp of the database if it is accessible.
The endpoint is accessible at `/health` and `/health/` (with or without a trailing slash).
"""

from datetime import datetime
from typing import Any
from fastapi import APIRouter, status
from api.database.postgresql import get_cursor
from api.management.schemas import HealthSchema, HealthStatus


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthSchema,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@router.get(
    "/",
    response_model=HealthSchema,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def health() -> HealthSchema:
    """
    Health check endpoint.
    Returns a JSON response with the status of the application and the current timestamp of the database if it is accessible.
    If the database connection is not working, the status will be `PG_DOWN` and the timestamp will be `None`.

    Returns:
        HealthSchema: A schema containing the status of the application and the current timestamp of the database if it is accessible.
    """
    status: HealthStatus = HealthStatus.UP
    timestamp: datetime | None = None
    try:
        async with get_cursor() as cursor:
            await cursor.execute("SELECT current_timestamp")
            result: tuple[Any, ...] | None = await cursor.fetchone()
            timestamp = result[0] if result else None

    except Exception as e:
        status = HealthStatus.PG_DOWN

    return HealthSchema(
        status=status,
        timestamp=timestamp,
    )


__all__: list[str] = [
    "router",
]
