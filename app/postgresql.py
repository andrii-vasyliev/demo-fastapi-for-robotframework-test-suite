"""
This module manages the asynchronous connection pool for PostgreSQL databases.
It provides functions to initialize, open, get cursor and close the connection pool.
"""

import contextlib
from typing import Any, AsyncIterator
from psycopg import AsyncCursor
from psycopg_pool import AsyncConnectionPool


__pool: AsyncConnectionPool | None = None


def setup_db_connection(db_url: str, pool_config: dict[str, Any] | None = None) -> None:
    global __pool
    if __pool is not None:
        raise Exception("PostgreSQL database is already initialized")

    if pool_config:
        pool_config.pop("conninfo", None)
        pool_config.pop("open", None)
    else:
        pool_config = {}

    __pool = AsyncConnectionPool(conninfo=db_url, open=False, **pool_config)


async def open_db_connection() -> None:
    if __pool is None:
        raise Exception("PostgreSQL database is not initialized")

    try:
        await __pool.open()
    except Exception as e:
        raise Exception("Unable to open PostgreSQL database pool:", e)


async def close_db_connection() -> None:
    global __pool
    if __pool is None:
        raise Exception("PostgreSQL database is not initialized")

    try:
        await __pool.close()
    except Exception as e:
        raise Exception("Unable to close PostgreSQL database pool", e)
    finally:
        __pool = None


@contextlib.asynccontextmanager
async def get_cursor() -> AsyncIterator[AsyncCursor]:
    if __pool is None:
        raise Exception("PostgreSQL database is not initialized")

    async with __pool.connection() as connection:
        async with connection.cursor() as cursor:
            try:
                yield cursor
            except Exception:
                await connection.rollback()
                raise
            else:
                await connection.commit()


__all__ = [
    "setup_db_connection",
    "open_db_connection",
    "get_cursor",
    "close_db_connection",
]
