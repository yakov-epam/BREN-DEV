from fastapi import Request, HTTPException
from fastapi.encoders import jsonable_encoder
from importlib.util import find_spec
from . import models

if find_spec("orjson") is not None:
    from fastapi.responses import ORJSONResponse as JSONResponse
else:
    from fastapi.responses import JSONResponse


async def handle_http_errors(_: Request, exc: HTTPException) -> JSONResponse:
    """
    HTTP error handler.
    :param _: FastAPI Request instance.
    :param exc: HTTPException instance.
    :return: Error response.
    """
    return JSONResponse(
        content=jsonable_encoder(
            models.ErrorResponse(message=exc.detail or "Something went wrong")
        ),
        status_code=exc.status_code,
    )
