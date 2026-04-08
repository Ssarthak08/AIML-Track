from pydantic import BaseModel, Field
from typing import Dict, Any
import uuid


class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    metadata: Dict[str, Any]  