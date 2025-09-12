from pydantic import BaseModel, Field


class BaseListResponse(BaseModel):
    total_pages: int = Field(title="Total pages")
