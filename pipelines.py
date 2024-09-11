from kfp.dsl import pipeline
from components import BaseKFComponent
from typing import Callable
from log_config import level

import inspect
import logging

logging.basicConfig(level=level)


class KFPipeline:
    def __init__(self, components: list[BaseKFComponent], **pipeline_parameters) -> None:
        self._components = components
        self._pipeline_params: dict = pipeline_parameters

    def make(self) -> Callable:
        @pipeline
        def pipeline_func(pipeline_params: dict = self._pipeline_params):
            roots = [root_component for root_component in self._components if root_component.prev == []]
            for root in roots:
                component = root
                while component.next != []:
                    params: dict = pipeline_params.get(component.component_name)
                    try:
                        params = {key: value["value"] for key, value in params}
                    except KeyError as e:
                        logging.error(f"[{__class__.__name__}] {e}")
                        raise e

                    task = component(**params)
                    component = component.next

        return pipeline_func

    def compile(self) -> None:
        pass

    def deploy(self) -> None:
        pass

    def run(self) -> None:
        pass
