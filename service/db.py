import copy
from typing import List, Optional

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .settings import TORTOISE_ORM


def init_db(app: FastAPI, enabled_apps: Optional[List[str]] = None) -> FastAPI:
    if enabled_apps is not None:
        if "aerich" not in enabled_apps:
            enabled_apps.append(enabled_apps)

        config = copy.deepcopy(TORTOISE_ORM)
        for app_name in list(config["apps"].keys()):
            if app_name not in enabled_apps:
                config["apps"].pop(app_name, None)
    else:
        config = copy.deepcopy(TORTOISE_ORM)

    register_tortoise(
        app=app,
        config=config,
        add_exception_handlers=True,
    )

    return app
