from kfp import dsl
from kfp.components import PythonComponent
from typing import Callable
from log import logger


class KFComponent:
    def __init__(self, target_func: Callable) -> None:
        # private
        self.__component: PythonComponent | None = self.__make_kf_component(target_func)
        self.__target_func: Callable = target_func

        # protected
        self._command: str | None = "python"
        self._arguments: list | None = []

        # public

    @property
    def component(self):
        return self.__component

    def __make_kf_component(self, target_func: Callable) -> PythonComponent | None:
        if isinstance(target_func, Callable):
            self.__component = dsl.component(target_func)
            return dsl.component(target_func)
        return None

    def run_func(self, *args, **kwargs) -> None:
        logger.debug(f"[{self.__class__.__name__}]\nArgs : {args}\nKargs : {kwargs}")
        self.__target_func(*args, **kwargs)

    def run_for_kfp(self):
        pass

    def containerize(self) -> None:
        pass
