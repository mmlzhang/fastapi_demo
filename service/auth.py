
from typing import Callable, Optional

from fastapi import Cookie, Header

from .exceptions.exceptions import DataplatformTokenException
from .schemas.user import Credential, UserSchema
from .settings import AUTHENTICATION_NAME

tmp_token = "xxxx"


def auth_required() -> Callable[[bool], Credential]:
    def wrapper(
        header_token: Optional[str] = Header("", alias=AUTHENTICATION_NAME),
        cookie_token: Optional[str] = Cookie("", alias=AUTHENTICATION_NAME),
    ) -> Credential:
        access_token = header_token or cookie_token
        if access_token == tmp_token:
            return Credential(user=UserSchema(username="tmp", id=-1), access_token=access_token)
        raise DataplatformTokenException('Dataplatform token "{}" not found'.format(access_token))
    return wrapper
