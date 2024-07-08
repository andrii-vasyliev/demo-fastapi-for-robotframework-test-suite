"""
Main API module
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse

from config import settings
from exceptions import AppException
from postgresql import connection_manager
from routers import customers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    https://fastapi.tiangolo.com/advanced/events/
    """
    connection_manager.setup(settings.database_url)
    await connection_manager.open()
    yield
    await connection_manager.close()


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=settings.debug,
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
    e = AppException(
        exc.status_code,
        [
            "http",
        ],
        "Not found",
        "not_found",
    )
    return JSONResponse(
        status_code=e.status_code,
        content=e.content(),
    )


@app.get("/", include_in_schema=False)
@app.get("/api/", include_in_schema=False)
async def read_root() -> RedirectResponse:
    return RedirectResponse(url=app.docs_url if app.docs_url else "/docs")


# Routers
app.include_router(customers_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        workers=settings.workers,
    )
