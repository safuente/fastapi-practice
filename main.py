import time

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.middleware.cors import CORSMiddleware

from auth import authentication
from db import models
from db.database import engine
from exceptions import StoryException
from router import blog_get, blog_post, user, article, product, file, template
from fastapi.staticfiles import StaticFiles
from custom_logger import setup_logging, logger

setup_logging()

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(article.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(template.router)



@app.get('/hello')
def index():
    logger.info("hello endpoint")
    return {'message': 'Hello world!'}


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={"detail": exc.name}

    )
"""
@app.exception_handler(HTTPException)
def custom_handler(request: Request, exc: StoryException):
    return PlainTextResponse(str(exc), status_code=400)
"""
models.Base.metadata.create_all(engine)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response



origins = [
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']

)

app.mount("/files", StaticFiles(directory="files"), name='files')
app.mount('/templates/static', StaticFiles(
    directory="templates/static"),
    name="static"
)







