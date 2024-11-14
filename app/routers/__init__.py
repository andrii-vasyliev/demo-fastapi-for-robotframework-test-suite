from .ping import router as ping_router
from .health import router as health_router
from .customers import router as customers_router

__all__ = [
    "ping_router",
    "health_router",
    "customers_router",
]
