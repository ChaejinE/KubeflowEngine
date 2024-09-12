from kfp.dsl import pipeline, PipelineTask
from components import BaseKFComponent
from typing import Callable
from log_config import level

import logging

logging.basicConfig(level=level)


class KFPipeline:
    def __init__(self, components: list[BaseKFComponent], **pipeline_parameters) -> None:
        self._components = components
        # self._pipeline_params: dict = self.parse_params_for_pipeline(pipeline_parameters)
        self._pipeline_params: dict = pipeline_parameters if pipeline_parameters else {}

    @staticmethod
    def parse_params_for_pipeline(src_params: dict[str, dict]) -> dict:
        dst_params: dict = {}
        if src_params:
            for component_name, param_dict in src_params.items():
                dst_params.update({component_name: {}})
                for key_, value_ in param_dict.items():
                    dst_params.get(component_name).update({key_: value_["value"]})

        logging.debug(f"[{__class__.__name__}] The parsed params is {dst_params}")

        return dst_params

    def make(self) -> Callable:
        @pipeline(name="my-pipeline")
        def pipeline_func(pipeline_params: dict = self._pipeline_params):
            roots = [root_component for root_component in self._components if root_component.prev == []]
            for root in roots:
                component = root

                while component.next != []:
                    component_arg_dict = {
                        key: value["value"]
                        for key, value in pipeline_params.get(component.component_name)
                        if pipeline_params.get("usage") == "input"
                    }
                    component.task = (
                        component.component(**component_arg_dict) if component_arg_dict else component.component()
                    )

                    prev_tasks: tuple[PipelineTask]
                    if component.prev:
                        if isinstance(component.prev, list):
                            prev_tasks = tuple([comp.task for comp in component.prev])
                        else:
                            prev_tasks = tuple(component.prev.task)

                    component.task.after(*prev_tasks)
                    component = component.next

        return pipeline_func

    def make_order_of_tasks(self, tasks: list[PipelineTask]):
        pass

    def compile(self) -> None:
        pass

    def deploy(self) -> None:
        pass

    def run(self) -> None:
        pass
