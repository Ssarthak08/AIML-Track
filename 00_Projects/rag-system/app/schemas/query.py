from pydantic import BaseModel, Field


class Query(BaseModel):
    question: str = Field(..., description="User query")
    top_k: int = Field(default=5, description="Number of chunks to retrieve")