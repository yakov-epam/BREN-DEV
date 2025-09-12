from .routes import ROUTER
from .auth import ROUTER as AUTH_ROUTER

ROUTER.include_router(AUTH_ROUTER)

__all__ = [
    "ROUTER",
]
