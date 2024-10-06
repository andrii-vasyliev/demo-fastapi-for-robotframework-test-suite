from .health import router as health_router
from .customers import router as customers_router

__all__ = [
    "health_router",
    "customers_router",
]
