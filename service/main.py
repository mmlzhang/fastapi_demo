"""Entrypoint, middleware and global exception handler includes"""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
# from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from .db import init_db
from .exceptions import error_handler_init
from .router import api
from .settings import SERVICE_URL_PREFIX, SHOW_API_DOC

if SHOW_API_DOC:
    openapi_url = f"{SERVICE_URL_PREFIX}/docsopenapi.json"
    docs_url = f"{SERVICE_URL_PREFIX}/docs"
    redoc_url = f"{SERVICE_URL_PREFIX}/redoc"
else:
    openapi_url = None
    docs_url = None
    redoc_url = None


app = FastAPI(
    openapi_url=openapi_url,
    openapi_prefix="",
    docs_url=docs_url,
    redoc_url=redoc_url,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app = init_db(app)
app = error_handler_init(app)


# app.mount("/static", StaticFiles(directory="service/www/dist"), name="static")
# app.mount("/js", StaticFiles(directory="service/www/dist/js"), name="js")
# app.mount("/css", StaticFiles(directory="service/www/dist/css"), name="css")
# app.mount("/assets", StaticFiles(directory="service/www/dist/assets"), name="assets")


origins = [
    "https://xxx.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api)
