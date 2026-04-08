from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_name: str
    content: str
    source: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))