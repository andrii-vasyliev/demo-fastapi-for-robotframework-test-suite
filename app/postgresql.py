import contextlib
from typing import Any, Annotated, AsyncIterator
from psycopg import AsyncCursor
from psycopg_pool import AsyncConnectionPool
from fastapi import Depends


class DatabaseConnectionManager:
    def __init__(self):
        self._pool: AsyncConnectionPool | None = None

    def setup(self, db_url: str, pool_config: dict[str, Any] = {}) -> None:
        if self._pool is not None:
            raise Exception("DatabaseConnectionManager is already initialized")

        pool_config.pop("conninfo", None)
        pool_config.pop("open", None)

        self._pool = AsyncConnectionPool(conninfo=db_url, open=False, **pool_config)

    async def open(self):
        if self._pool is None:
            raise Exception("DatabaseConnectionManager is not initialized")

        await self._pool.open()

    async def close(self):
        if self._pool is None:
            raise Exception("DatabaseConnectionManager is not initialized")

        await self._pool.close()
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
