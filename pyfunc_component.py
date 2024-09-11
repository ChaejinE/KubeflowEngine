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
        self._component: PythonComponent | None = None
        # public

    @property
    def component(self) -> PythonComponent | None:
        return self._make_kf_component(self._target_func)

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
        logging.debug(
            f"[{__class__.__name__}] The packages to install will be changed from {self._packages_to_install} to {packages_list}"
        )
        self._packages_to_install = packages_list

    def set_attr_for_user(
        self,
        base_image: str | None = None,
        registry: str | None = None,
        component_name: str | None = None,
        version: str | None = None,
        kfp_package_path: str | None = None,
        packages_to_install: list[str] | None = None,
    ) -> None:
        self._base_image = base_image if isinstance(base_image, str) else self._base_image
        self._registry = registry if isinstance(registry, str) else self._registry
        self._component_name = component_name if isinstance(component_name, str) else self._component_name
        self._version = version if isinstance(version, str) else self._version
        self._kfp_package_path = kfp_package_path if isinstance(kfp_package_path, str) else self._kfp_package_path
        self._packages_to_install = (
            packages_to_install if isinstance(packages_to_install, list) else self._packages_to_install
        )

    def _make_kf_component(self, target_func: Callable) -> PythonComponent | None:
        if isinstance(target_func, Callable):
            if self._kfp_package_path is not None and not (os.path.exists(path=self._kfp_package_path)):
                raise FileExistsError(f"\n[{self.__class__.__name__}] There isn't a requirements file")

            logging.info(f"[{__class__.__name__}] The target function is the {target_func.__name__}")
            logging.info(f"[{__class__.__name__}] The base image is a {self._base_image}")
            logging.info(f"[{__class__.__name__}] The target image is a {self._target_image}")
            logging.info(f"[{__class__.__name__}] The packages to install are {self._packages_to_install}")
            return dsl.component(
                func=target_func,
                base_image=self._base_image,
                target_image=self._target_image,
                kfp_package_path=self._kfp_package_path,
                packages_to_install=self._packages_to_install,
            )

        logging.debug(f"[{self.__class__.__name__}] The target_func isn't callable : {type(target_func)}")
        return None

    def run_target_func(self, *args, **kwargs) -> Any | None:
        try:
            logging.debug(f"[{self.__class__.__name__}] Target Function runs\nArgs : {args}\nKwargs : {kwargs}")
            result = self._target_func(*args, **kwargs)
            logging.debug(f"[{self.__class__.__name__}] End\nResult Type : {type(result)}\nResult : {result}")
        except Exception as e:
            logging.debug(f"[{self.__class__.__name__}] Raised Error\n{e}")
            result = None

        return self._target_func(*args, **kwargs)

    def build_image(self, target_component_path: str) -> None:
        logging.debug(f"[{__class__.__name__}] The component's path is a {target_component_path}")
        directory, filename = os.path.dirname(target_component_path), os.path.basename(target_component_path)
        cmd = f"kfp component build {directory} --component-filepattern {filename} --no-push-image"
        logging.info(f"[{__class__.__name__}] The build command is a '{cmd}'")

        logging.info(f"[{__class__.__name__}] Build Start")
        os.system(f"{cmd}")
        logging.info(f"[{self.__class__.__name__}] Build End")

    def push_image(self, target_component_path: str) -> None:
        directory, filename = os.path.dirname(target_component_path), os.path.basename(target_component_path)
        cmd = f"kfp component build {directory} --component-filepattern {filename} --push-image"
        logging.info(f"[{__class__.__name__}] The push command is a '{cmd}'")

        logging.info(f"[{__class__.__name__}] Push Start")
        os.system(f"{cmd}")
        logging.info(f"[{self.__class__.__name__}] Push End")
