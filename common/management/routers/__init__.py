from .health import router as health_router
from .ping import router as ping_router

__all__: list[str] = [
    "health_router",
    "ping_router",
]
