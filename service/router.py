from fastapi import APIRouter

from .settings import SERVICE_URL_PREFIX
from .views.index import index_router

api = APIRouter(prefix=SERVICE_URL_PREFIX)

api.include_router(index_router, prefix="", tags=['首页'])
