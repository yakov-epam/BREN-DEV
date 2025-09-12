from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(title="Declares if the app is healthy", default="ok")
