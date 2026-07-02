from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI() # creating the instance 

templates = Jinja2Templates(directory="templates")

# uv run fastapi dev main.py and uv run fastapi:main --reload, 2 commands one for local env and other for production. --reload automatically reloads the server when any changes are made in the file. 

# curl command - Client url used for directly sending HTTP requests through terminal only. 

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",{"posts": posts})

@app.get("/api/posts")
def get_post():
    return posts