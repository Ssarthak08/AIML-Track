from pydantic import BaseModel
from typing import List


class Source(BaseModel):
    source: str
    page: int
    content: str


class Response(BaseModel):
    answer: str
    sources: List[Source]