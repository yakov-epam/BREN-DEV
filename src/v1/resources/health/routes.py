from fastapi import APIRouter
from . import schemas
from .schemas import HealthResponse

ROUTER = APIRouter(prefix="/health", tags=["Health"])


@ROUTER.get(
    path="",
    name="Health",
    responses={200: {"model": HealthResponse, "description": "Application is healthy"}},
)
async def _():
    return schemas.HealthResponse()
