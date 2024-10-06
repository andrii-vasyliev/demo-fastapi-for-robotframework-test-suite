"""
This module provides a class `DatabaseConnectionManager` to manage the connection pool
for PostgreSQL database connections. It includes methods to initialize the connection pool,
open and close the pool, and obtain a cursor context manager.

The `get_cursor` function is a dependency function that provides an asynchronous cursor
context manager using the connection pool.
"""

import contextlib
from typing import Any, Annotated, AsyncIterator
from psycopg import AsyncCursor
from psycopg_pool import AsyncConnectionPool
from fastapi import Depends


class DatabaseConnectionManager:
    def __init__(self) -> None:
        self._pool: AsyncConnectionPool | None = None

    def setup(self, db_url: str, pool_config: dict[str, Any] | None = None) -> None:
        if self._pool is not None:
            raise Exception("DatabaseConnectionManager is already initialized")

        if pool_config:
            pool_config.pop("conninfo", None)
            pool_config.pop("open", None)
        else:
            pool_config = {}

        self._pool = AsyncConnectionPool(conninfo=db_url, open=False, **pool_config)

    async def open(self) -> None:
        if self._pool is None:
            raise Exception("DatabaseConnectionManager is not initialized")

        try:
            await self._pool.open()
        except Exception as e:
            raise Exception("Unable to open DatabaseConnectionManager pool:", e)

    async def close(self) -> None:
        if self._pool is None:
            raise Exception("DatabaseConnectionManager is not initialized")

        try:
            await self._pool.close()
        except Exception as e:
            raise Exception("Unable to close DatabaseConnectionManager pool", e)
        finally:
            self._pool = None

    @contextlib.asynccontextmanager
    async def cursor(self) -> AsyncIterator[AsyncCursor]:
        if self._pool is None:
            raise Exception("DatabaseConnectionManager is not initialized")

        async with self._pool.connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    yield cursor
                except Exception:
                    await connection.rollback()
                    raise
                else:
                    await connection.commit()


connection_manager: DatabaseConnectionManager = DatabaseConnectionManager()


async def get_cursor() -> AsyncIterator[AsyncCursor]:
    async with connection_manager.cursor() as cursor:
        yield cursor


Cursor = Annotated[AsyncCursor, Depends(get_cursor)]

__all__ = [
    "connection_manager",
    "Cursor",
]
