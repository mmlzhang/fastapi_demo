
from fastapi import APIRouter

index_router = APIRouter()


@index_router.get(
    "/health",
    summary='健康检查接口',
    description='服务内部健康检查/k8s服务探针'
)
async def health():
    return {"code": 200, 'msg': "OK"}
