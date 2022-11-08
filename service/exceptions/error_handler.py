
import traceback

from fastapi import Request
from starlette.responses import JSONResponse

from .exceptions import CustomException


def error_handler_init(app):

    @app.exception_handler(CustomException)
    async def http_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        return JSONResponse(
            {
                "code": exc.code,
                "message": exc.message,
            },
            status_code=exc.status_code or 400,
        )

    @app.exception_handler(Exception)
    async def common_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        traceback.print_exception(type(exc), exc, exc.__traceback__)
        # wecom = WeCom()
        # wecom.error(title='内部服务器错误', text=traceback.format_exc())
        return JSONResponse(
            {
                "code": 500,
                "message": "内部服务器错误",
            },
            status_code=500,
        )

    return app
