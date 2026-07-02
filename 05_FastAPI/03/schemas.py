from pydantic import BaseModel

class Books(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str 
    page_count: int
    language: str


class BookupdateModel(BaseModel):
    title: str | None = None
    publisher: str | None = None
    page_count: int | None = None
    language: str | None = None
