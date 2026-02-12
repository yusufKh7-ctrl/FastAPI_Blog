from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome", 
        "content": "This framework is really casy to use and super fast.",
        "date_posted": "April 20, 2025"
    },
    {
    "id": 2,
    "author": "Jane Doe",
    "title": "Python is Great for Web Development", 
    "content": "Python is a great language for web development, and FastAPI makes it even better.", 
    "date_posted": "April 21, 2025"
    },
]

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, 
        "home.html",
        {"posts": posts, "title": "Home"}
    )


@app.get("/post/{post_id}")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post["id"] == post_id:
                title = post['title'][:20] + "..." if len(post['title']) > 20 else post["title"]
                return templates.TemplateResponse(
                request, 
                "post.html",
                {"post": post, "title": title}
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/api/posts")
def get_posts():
    return posts


@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException):
    message = (
        exc.detail if exc.detail else "An error occurred."
    )
    
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": message}
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exc.status_code,
            "title": exc.status_code,
            "message": message
        },
        status_code=exc.status_code,
    )
    
# RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exc.errors()}
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": "Invalid Request Data",
            "message": "Invalid request data. Please check your input and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )