from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from const import SETTINGS, AppEnv, DATABASE
from contextlib import asynccontextmanager
from importlib.util import find_spec
from v1 import create_v1_app
import error_handlers

# Speedups
if find_spec("orjson") is not None:
    from fastapi.responses import ORJSONResponse as JSONResponse
else:
    from fastapi.responses import JSONResponse

if find_spec("uvloop") is not None:
    import uvloop
    import asyncio

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# End speedups


@asynccontextmanager
async def lifecycle(_: FastAPI) -> AsyncGenerator[None]:
    """
    Application lifecycle manager.
    All instructions before `yield` will run on startup.
    The ones after `yield` will run on shutdown.
    :param _: FastAPI instance.
    :return: None.
    """
    # Startup
    yield
    # Shutdown
    DATABASE.engine.dispose()


def create_app() -> FastAPI:
    """
    FastAPI application factory.
    :return: FastAPI instance.
    """
    app = FastAPI(
        title=SETTINGS.app.title,
        docs_url=None if SETTINGS.app.disable_swagger else "/docs",
        redoc_url=None if SETTINGS.app.disable_redoc else "/redoc",
        default_response_class=JSONResponse,
        lifespan=lifecycle,
    )
    app.add_exception_handler(HTTPException, error_handlers.handle_http_errors)  # noqa
    app.mount("/v1", create_v1_app(), name="V1")
    return app


if __name__ == "__main__":
    if SETTINGS.env == AppEnv.DEV:
        import uvicorn

        uvicorn.run(
            "main:create_app",
            factory=True,
            host=SETTINGS.app.host,
            port=SETTINGS.app.port,
            reload=True,
        )
    else:
        import granian

        granian.Granian(
            address=SETTINGS.app.host,
            port=SETTINGS.app.port,
            reload=False,
        ).serve()
