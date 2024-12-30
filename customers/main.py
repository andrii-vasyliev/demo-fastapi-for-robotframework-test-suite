"""
Main API application module
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse

from customers.config import settings
from common.exceptions import AppException, HTTP_NOT_FOUND
from common.database.postgresql import (
    init_db_connection,
    open_db_connection,
    close_db_connection,
)
from common.management.routers import health_router, ping_router
from customers.routers import customers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    https://fastapi.tiangolo.com/advanced/events/
    """
    init_db_connection(settings.database_url)
    await open_db_connection()
    yield
    await close_db_connection()


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=settings.debug,
    title=settings.title,
    description=settings.description,
    version=settings.version,
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content(),
    )


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def http_404_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_NOT_FOUND.status_code,
        content=HTTP_NOT_FOUND.content(),
    )


@app.get("/", include_in_schema=False)
@app.get("/api/", include_in_schema=False)
async def read_root() -> RedirectResponse:
    return RedirectResponse(url=app.docs_url if app.docs_url else "/docs")


# Routers
app.include_router(ping_router, include_in_schema=False)
app.include_router(health_router, include_in_schema=False)
app.include_router(customers_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="customers.main:app",
        workers=settings.workers,
        reload=settings.reload if settings.workers <= 1 else False,
        host=settings.host,
        port=settings.port,
    )
