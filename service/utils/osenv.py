
import json
import os
import sys
import threading
from typing import Any, Callable, Optional, TypeVar

import logbook

DEBUG = os.getenv("DEBUG", False)
T = TypeVar("T")


class Logger(object):

    mutex = threading.Lock()
    singleton = None
    logger = None

    @staticmethod
    def get_instance():
        """sington, create logger
        """
        if not Logger.singleton:
            Logger.mutex.acquire()
            if not Logger.singleton:
                Logger.singleton = Logger()
            Logger.mutex.release()
        return Logger.singleton

    def __init__(self, project='OSEnv', debug=DEBUG):
        self.logger = logbook.Logger(project)
        logbook.set_datetime_format('local')
        self.logger.handlers.append(logbook.StreamHandler(sys.stdout))
        self.logger.level = logbook.INFO
        if debug:
            self.logger.level = logbook.DEBUG


class OSEnv:
    @classmethod
    def general_loader(
        cls: "OSEnv",
        name: str,
        loader: Callable[[str], T],
        default: T,
        description: Optional[str] = None,
    ) -> T:
        value = os.getenv(name, None)
        value = (value and loader(value)) or default
        cls.log(name=name, value=value, use_default=bool(value), description=description)
        return value

    @staticmethod
    def log(
        name: str,
        value: Any,
        use_default: bool,
        description: Optional[str] = None,
    ) -> None:
        if type(value) == str:
            value = f'"{value}"'
        value = f"{value} ({type(value).__name__})"
        log = Logger.get_instance().logger
        log.debug(f"{name.ljust(35)} --> {value} ({'default' if use_default else 'env'}) ({description})")

    @classmethod
    def int(
        cls: "OSEnv",
        name: str,
        default: int = 0,
        description: Optional[str] = None,
    ) -> int:
        return cls.general_loader(
            name=name,
            loader=lambda v: int(v),
            default=default,
            description=description,
        )

    @classmethod
    def float(
        cls: "OSEnv",
        name: str,
        default: float = 0.0,
        description: Optional[str] = None,
    ) -> float:
        return cls.general_loader(
            name=name,
            loader=lambda v: float(v),
            default=default,
            description=description,
        )

    @classmethod
    def bool(
        cls: "OSEnv",
        name: str,
        default: bool = False,
        description: Optional[str] = None,
    ) -> bool:
        return cls.general_loader(
            name=name,
            loader=lambda v: v.lower() in ["true", "1", "yes"],
            default=default,
            description=description,
        )

    @classmethod
    def json(
        cls: "OSEnv",
        name: str,
        default: Optional[Any] = None,
        description: Optional[str] = None,
    ) -> Any:
        return cls.general_loader(
            name=name,
            loader=lambda v: json.loads(v),
            default=default,
            description=description,
        )

    # move this to bottom
    @classmethod
    def str(
        cls: "OSEnv",
        name: str,
        default: str = "",
        description: Optional[str] = None,
    ) -> str:
        return cls.general_loader(
            name=name,
            loader=lambda v: str(v),
            default=default,
            description=description,
        )
