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
from fastapi import APIRouter, Request, status
from app.postgresql import Cursor
from app.schemas import HealthStatus, HealthSchema


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
async def health(cursor: Cursor, request: Request) -> HealthSchema:
    """
    Health Check
    """
    status: HealthStatus = HealthStatus.UP
    timestamp: datetime | None = None
    try:
        await cursor.execute("SELECT current_timestamp")
        result: tuple[Any, ...] | None = await cursor.fetchone()
        timestamp = result[0] if result else None
    except Exception as e:
        status = HealthStatus.PG_DOWN

    return HealthSchema(
        status=status,
        timestamp=timestamp,
    )


__all__ = [
    "router",
]
