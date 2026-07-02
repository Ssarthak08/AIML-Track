from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from typing import List
from schemas import Books, BookupdateModel
from book_data import books



app = FastAPI()








@app.get('/books', response_model=list[Books])
async def get_all_books() -> list:
    return books

@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Books) -> dict:
    new_book = book_data.model_dump() # coversion of object to dict
    books.append(new_book)
    return new_book

@app.get('/book/{book_id}')
async def get_book(book_id : int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.patch('/book/{book_id}')
async def update_book(book_id : int, bookupdatedata : BookupdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = bookupdatedata.title
            book['publisher'] = bookupdatedata.publisher
            book['page_count'] = bookupdatedata.page_count
            book['language'] = bookupdatedata.language

            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    


@app.delete('/book/{book_id}')
async def delete_book(book_id : int) -> dict:
    pass 