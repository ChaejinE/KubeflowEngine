from kfp import dsl
from kfp.components import PythonComponent
from typing import Callable, Any
from log_config import level

import logging, os

logging.basicConfig(level=level)


class KFPythonFuncComponent:
    def __init__(self, target_func: Callable) -> None:
        # private
        # protected
        self._target_func: Callable = target_func
        self._base_image: str | None = "python:3.9-slim"
        self._registry: str | None = "129231402580.dkr.ecr.us-east-1.amazonaws.com/components_luke"
        self._component_name: str | None = "test"
        self._version: str | None = "v1"
        self._target_image: str | None = f"{self._registry}:{self._component_name}-{self._version}"
        self._kfp_package_path: str | None = None
        self._packages_to_install: list[str] | None = None
        self._command: str | None = "python"
        self._arguments: list | None = []
        self._component: PythonComponent | None = self._make_kf_component(target_func)
        # public

    @property
    def component(self) -> PythonComponent | None:
        return self._component

    @property
    def base_image(self) -> str | None:
        return self._base_image

    @base_image.setter
    def base_image(self, image_name: str):
        self._base_image = image_name

    @property
    def registry(self) -> str | None:
        return self._registry

    @registry.setter
    def registry(self, name: str):
        self._registry = name

    @property
    def component_name(self) -> str | None:
        return self._component_name

    @component_name.setter
    def component_name(self, name: str):
        self._component_name = name

    @property
    def version(self) -> str | None:
        return self._version

    @version.setter
    def version(self, version: str):
        self._version = version

    @property
    def packages_to_install(self) -> list[str] | None:
        return self._packages_to_install

    @packages_to_install.setter
    def packages_to_install(self, packages_list: list[str]):
        self._packages_to_install = packages_list

    def _make_kf_component(self, target_func: Callable) -> PythonComponent | None:
        if isinstance(target_func, Callable):
            if self._kfp_package_path is not None and not (os.path.exists(path=self._kfp_package_path)):
                raise FileExistsError(f"\n[{self.__class__.__name__}] There isn't a requirements file")

            return dsl.component(
                func=target_func,
                base_image=self._base_image,
                target_image=self._target_image,
                kfp_package_path=self._kfp_package_path,
                packages_to_install=self._packages_to_install,
            )

        logging.debug(f"\n[{self.__class__.__name__}] The target_func isn't callable : {type(target_func)}")
        return None

    def run_target_func(self, *args, **kwargs) -> Any | None:
        try:
            logging.debug(f"\n[{self.__class__.__name__}] Target Function runs\nArgs : {args}\nKwargs : {kwargs}")
            result = self._target_func(*args, **kwargs)
            logging.debug(f"\n[{self.__class__.__name__}] End\nResult Type : {type(result)}\nResult : {result}")
        except Exception as e:
            logging.debug(f"\n[{self.__class__.__name__}] Raised Error\n{e}")
            result = None

        return self._target_func(*args, **kwargs)

    def build(self) -> None:
        component = self.component  # Stay this code
        tmp_file_path = "tmp_component.py"
        component_path = "example.py"
        with open(tmp_file_path, "w") as f:
            import_filename = os.path.basename(__file__)
            logging.debug(f"\n[{self.__class__.__name__}] filename: {import_filename}")
            ext_len = len(import_filename.split(".")[-1]) + 1
            f.write(
                f"from {import_filename[:-1*ext_len]} import {__class__.__name__}\nfrom {component_path[:-1*ext_len]} import {self._target_func.__name__}\ncomponent = {__class__.__name__}({self._target_func.__name__}).component"
            )

        os.system(f"kfp component build ./ --component-filepattern {tmp_file_path} --no-push-image")
        os.remove(tmp_file_path)
