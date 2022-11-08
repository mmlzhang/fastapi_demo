
class CustomException(Exception):
    """
    自定义异常类

        后面的自定义异常都需要继承自这个类

    """

    # http状态码, 一般不用修改
    status_code: int = 400
    # 返回json数据中的code
    code: int = 10000

    def __init__(self: "CustomException", message: str) -> None:
        self.message = message


class UnauthorizedException(CustomException):
    """登录认证异常"""
    status_code = 401
    code = 40001


class DataplatformTokenException(CustomException):
    """Dataplatform token错误"""
    status_code = 401
    code = 40002


class NotFundException(CustomException):
    """不存在"""
    code = 50002


class AlreadyExistsException(CustomException):
    """已存在不能重复"""
    code = 50003


class DataPreviewException(CustomException):
    """Dataplatform预览错误"""
    code = 50005


class StatusErrorException(CustomException):
    """状态错误"""
    code = 50006
