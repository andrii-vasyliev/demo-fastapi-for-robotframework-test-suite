"""
This module contains the ping router for the API.
It provides a simple endpoint to check if the API is running and responding.
The endpoint is accessible at `/ping` and `/ping/` (with or without a trailing slash).
"""

from typing import Any
from fastapi import APIRouter, Request, Response, status


router = APIRouter(
    prefix="/ping",
    tags=["Ping"],
)


@router.get(
    "",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
@router.get(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
async def ping(request: Request) -> Any:
    """
    Simple service availability check
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


__all__ = [
    "router",
]
