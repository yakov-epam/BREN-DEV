from fastapi import FastAPI, HTTPException
import error_handlers
from const import SETTINGS
from . import resources
from importlib.util import find_spec

if find_spec("orjson") is not None:
    from fastapi.responses import ORJSONResponse as JSONResponse
else:
    from fastapi.responses import JSONResponse


def create_v1_app() -> FastAPI:
    """
    FastAPI application factory.
    :return: FastAPI application.
    """
    app_ = FastAPI(
        title=SETTINGS.app.title,
        docs_url=None if SETTINGS.app.disable_swagger else "/docs",
        redoc_url=None if SETTINGS.app.disable_redoc else "/redoc",
        default_response_class=JSONResponse,
        version=SETTINGS.app.latest_v1,
    )
    app_.add_exception_handler(HTTPException, error_handlers.handle_http_errors)  # noqa
    app_.include_router(resources.health.ROUTER)
    app_.include_router(resources.books.ROUTER)
    return app_
