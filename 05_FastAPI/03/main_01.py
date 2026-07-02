from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Message": "hello world"}

@app.get("/greet")
async def greet_name(name:Optional[str] = "User", age: int = 0)-> dict:
    return {"Message": f"Hello {name}, age : {age}"}


class Bookcreatemodel(BaseModel):
    title : str 
    author : str 

@app.post("/create_book")
async def create_book(Book_data : Bookcreatemodel):
    return {
        "title_of_the_book": Book_data.title,
        "author_of_the_book": Book_data.author  
    } 

@app.get("/get_headers")
async def get_headers():
    pass